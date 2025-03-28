import requests
import time
import json
import logging
import csv
from tqdm import tqdm

# Configuracao basica do logging
logging.basicConfig(
    filename='processamento.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Funcao para consultar o CNPJ usando a API MinhaReceita com tentativas de repeticao
def consultar_cnpj(cnpj, max_retries=3, retry_delay=5):
    base_url = "https://minhareceita.org/"
    url = f"{base_url}{cnpj}"
    
    attempts = 0
    while attempts < max_retries:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                logging.info(f"CNPJ {cnpj} consultado com sucesso.")
                return response.json()
            elif response.status_code == 404:
                attempts += 1
                logging.warning(f"CNPJ {cnpj} nao encontrado. Tentativa {attempts} de {max_retries}.")
                if attempts < max_retries:
                    logging.info(f"Aguardando {retry_delay} segundos antes de tentar novamente...")
                    time.sleep(retry_delay)
                else:
                    logging.error(f"Falha ao consultar CNPJ {cnpj} apos {max_retries} tentativas. Status Code: 404")
                    return None
            else:
                logging.error(f"Erro ao consultar CNPJ {cnpj}: Status Code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            attempts += 1
            logging.error(f"Tentativa {attempts} falhou ao consultar CNPJ {cnpj}: {e}")
            if attempts < max_retries:
                logging.info(f"Aguardando {retry_delay} segundos antes de tentar novamente...")
                time.sleep(retry_delay)
            else:
                logging.error(f"Falha ao consultar CNPJ {cnpj} apos {max_retries} tentativas. Erro: {e}")
                return None

# Funcao para criar CSV a partir do JSON
def criar_csv_a_partir_de_json(arquivo_json, arquivo_csv_saida):
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as file:
            dados = json.load(file)
    except FileNotFoundError:
        logging.error(f"Arquivo JSON {arquivo_json} nao encontrado.")
        return
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao decodificar o JSON: {e}")
        return

    campos = [
        "cnpj",
        "descricao_identificador_matriz_filial",
        "nome_fantasia",
        "descricao_situacao_cadastral",
        "data_situacao_cadastral",
        "descricao_motivo_situacao_cadastral",
        "cnae_fiscal",
        "cnae_fiscal_descricao",
        "uf",
        "municipio",
        "razao_social",
        "porte"
    ]

    try:
        with open(arquivo_csv_saida, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=campos, delimiter=';')
            writer.writeheader()
            for item in dados:
                writer.writerow({
                    campo: item.get(campo, "") for campo in campos
                })
        logging.info(f"Arquivo CSV {arquivo_csv_saida} criado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo CSV: {e}")

# Funcao principal
def main():
    caminho_entrada = r'/home/geraldo.junior/Database_mkt/etl/Atualiza_cnae/resultado/Lista_de_cnpj.csv'

    try:
        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        logging.info(f"Arquivo {caminho_entrada} carregado com sucesso.")
    except FileNotFoundError:
        logging.error(f"Arquivo {caminho_entrada} nao encontrado.")
        print(f"Arquivo {caminho_entrada} nao encontrado.")
        return
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo: {e}")
        print(f"Erro ao ler o arquivo: {e}")
        return

    cnpjs = [linha.strip() for linha in linhas if linha.strip()]
    if not cnpjs:
        logging.warning("Nenhum CNPJ encontrado no arquivo.")
        print("Nenhum CNPJ encontrado no arquivo.")
        return

    resultados = []
    delay_entre_requisicoes = 1

    with tqdm(total=len(cnpjs), desc="Processando CNPJs", unit="CNPJ") as pbar:
        for cnpj in cnpjs:
            cnpj = ''.join(filter(str.isdigit, cnpj)).zfill(14)

            if len(cnpj) != 14:
                logging.warning(f"CNPJ invalido encontrado: {cnpj}")
                pbar.set_postfix({'Status': 'CNPJ Invalido'})
                pbar.update(1)
                continue

            resultado = consultar_cnpj(cnpj)
            if resultado:
                registro = {
                    "cnpj": resultado.get("cnpj", ""),
                    "descricao_identificador_matriz_filial": resultado.get("descricao_identificador_matriz_filial", ""),
                    "nome_fantasia": resultado.get("nome_fantasia", ""),
                    "descricao_situacao_cadastral": resultado.get("descricao_situacao_cadastral", ""),
                    "data_situacao_cadastral": resultado.get("data_situacao_cadastral", ""),
                    "descricao_motivo_situacao_cadastral": resultado.get("descricao_motivo_situacao_cadastral", ""),
                    "cnae_fiscal": resultado.get("cnae_fiscal", ""),
                    "cnae_fiscal_descricao": resultado.get("cnae_fiscal_descricao", ""),
                    "uf": resultado.get("uf", ""),
                    "municipio": resultado.get("municipio", ""),
                    "razao_social": resultado.get("razao_social", ""),
                    "porte": resultado.get("porte", "")
                }
                resultados.append(registro)

            pbar.set_postfix({'Status': 'Processando'})
            pbar.update(1)
            time.sleep(delay_entre_requisicoes)

    if not resultados:
        logging.warning("Nenhum resultado obtido das consultas.")
        print("Nenhum resultado obtido das consultas.")
        return

    arquivo_json = r'/home/geraldo.junior/Database_mkt/etl/Atualiza_cnae/resultado/ResultadoJson.json'
    try:
        with open(arquivo_json, 'w', encoding='utf-8') as file:
            json.dump(resultados, file, ensure_ascii=False, indent=4)
        logging.info(f"Arquivo JSON {arquivo_json} criado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo JSON: {e}")
        print(f"Erro ao salvar o arquivo JSON: {e}")
        return

    arquivo_csv_saida = r'/home/geraldo.junior/Database_mkt/etl/Atualiza_cnae/resultado/Arquivo_para_upload_Big_query.csv'
    criar_csv_a_partir_de_json(arquivo_json, arquivo_csv_saida)

    print("Processo concluido. Verifique o arquivo final CSV.")
    logging.info("Processo concluido com sucesso.")

if __name__ == "__main__":
    main()
