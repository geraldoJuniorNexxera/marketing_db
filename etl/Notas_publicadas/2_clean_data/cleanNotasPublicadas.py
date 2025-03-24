import os
import pandas as pd
import csv
from datetime import datetime
import warnings

# Suprimir avisos do openpyxl
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

# Caminho da pasta onde os arquivos .xlsx estão localizados
pasta_downloads = r"C:\Users\geraldo.junior\Downloads"

# Caminho do arquivo CSV de saída
output_file_path = r"C:\Users\geraldo.junior\Downloads\notas_limpas.csv"

# Colunas que devem ser mantidas
colunas_mantidas = [
    "id_nota", 
    "sacado", 
    "vl_documento", 
    "dt_inclusao", 
    "cedente", 
    "cnpj_cedente", 
    "dt_vcto", 
    "dt_emissao"
]

# Função para formatar datas no formato YYYY-MM-DD
def formatar_data(data):
    if pd.isna(data):  # Verifica se o valor é NaN (nulo)
        return None
    if isinstance(data, pd.Timestamp):  # Verifica se é um objeto Timestamp
        return data.strftime("%Y-%m-%d")  # Converte para string no formato YYYY-MM-DD
    if isinstance(data, str):  # Verifica se é uma string
        try:
            # Tenta converter a string para datetime e depois formata
            data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
            return data_formatada
        except ValueError:
            # Se falhar, tenta outros formatos de data
            try:
                data_formatada = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
                return data_formatada
            except ValueError:
                return None  # Retorna None se não conseguir converter
    return None  # Retorna None para outros tipos de dados

# Função para converter valores numéricos
def converter_valores(item):
    # Converte "cnpj_cedente" para NUMERIC (int ou float)
    if "cnpj_cedente" in item and item["cnpj_cedente"] is not None and item["cnpj_cedente"] != "":
        try:
            item["cnpj_cedente"] = int(float(item["cnpj_cedente"]))  # Converte para int (NUMERIC)
        except (ValueError, TypeError):
            item["cnpj_cedente"] = None  # Se falhar, define como None
    # Converte "vl_documento" para FLOAT64
    if "vl_documento" in item and item["vl_documento"] is not None and item["vl_documento"] != "":
        try:
            item["vl_documento"] = float(item["vl_documento"])  # Converte para float (FLOAT64)
        except (ValueError, TypeError):
            item["vl_documento"] = None  # Se falhar, define como None
    # Garante que "id_nota" seja um número (sem aspas)
    if "id_nota" in item and item["id_nota"] is not None and item["id_nota"] != "":
        try:
            item["id_nota"] = int(float(item["id_nota"]))  # Tenta converter para int
        except (ValueError, TypeError):
            item["id_nota"] = None  # Se falhar, define como None
    return item

# Função para limpar os dados
def limpar_csv(data, colunas_mantidas):
    dados_limpos = []
    for item in data:
        item_limpo = {coluna: item.get(coluna) for coluna in colunas_mantidas}
        # Formata as colunas de data para o formato YYYY-MM-DD
        for coluna_data in ["dt_vcto", "dt_inclusao", "dt_emissao"]:
            if coluna_data in item_limpo:
                item_limpo[coluna_data] = formatar_data(item_limpo[coluna_data])
        # Converte os valores numéricos
        item_limpo = converter_valores(item_limpo)
        dados_limpos.append(item_limpo)
    return dados_limpos

# Listar todos os arquivos .xlsx na pasta de downloads
arquivos_xlsx = [arquivo for arquivo in os.listdir(pasta_downloads) if arquivo.endswith('.xlsx')]

# Verificar se há arquivos .xlsx na pasta
if not arquivos_xlsx:
    print("Nenhum arquivo .xlsx encontrado na pasta.")
    exit()

# Ler o primeiro arquivo .xlsx encontrado (ou você pode iterar sobre todos)
input_file_path = os.path.join(pasta_downloads, arquivos_xlsx[0])

# Ler o arquivo Excel
try:
    df = pd.read_excel(input_file_path)
    dados = df.to_dict('records')  # Converte o DataFrame para uma lista de dicionários
except Exception as e:
    print(f"Erro ao ler o arquivo Excel: {e}")
    exit()

# Limpar os dados
dados_limpos = limpar_csv(dados, colunas_mantidas)

# Função para verificar se os campos são repetidos
def campos_repetidos(item1, item2):
    campos_verificar = ["vl_documento", "cnpj_cedente", "dt_vcto", "dt_emissao"]
    for campo in campos_verificar:
        if item1.get(campo) != item2.get(campo):
            return False
    return True

# Filtrar os dados para "GM - GENERAL MOTORS DO BRASIL LTDA"
dados_gm = [item for item in dados_limpos if item.get("sacado") == "GM - GENERAL MOTORS DO BRASIL LTDA"]

# Agrupar os dados do sacado "GM - GENERAL MOTORS DO BRASIL LTDA" com base nos campos repetidos e manter a linha com a "dt_inclusao" mais recente
dados_gm_agrupados = {}
for item in dados_gm:
    chave = tuple(item[campo] for campo in ["vl_documento", "cnpj_cedente", "dt_vcto", "dt_emissao"])
    dt_inclusao = item["dt_inclusao"]
    if chave not in dados_gm_agrupados or dt_inclusao > dados_gm_agrupados[chave]["dt_inclusao"]:
        dados_gm_agrupados[chave] = item

# Converter o dicionário de volta para uma lista
dados_gm_filtrados = list(dados_gm_agrupados.values())

# Combinar os dados filtrados com o restante dos dados (outros sacados)
dados_finais = [item for item in dados_limpos if item.get("sacado") != "GM - GENERAL MOTORS DO BRASIL LTDA"]
dados_finais.extend(dados_gm_filtrados)

# Salvar o novo arquivo CSV com delimitador ;
try:
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=colunas_mantidas, delimiter=';')
        writer.writeheader()  # Escreve o cabeçalho (nomes das colunas)
        writer.writerows(dados_finais)  # Escreve as linhas de dados
    print(f"Arquivo CSV limpo salvo com sucesso em: {output_file_path}")
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV limpo: {e}")