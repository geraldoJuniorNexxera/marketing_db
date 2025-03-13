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
    "ds_razaosocial_forn", "dt_vcto", "nu_nf", "nu_cpfcnpj_comp", 
    "dt_inclusao", "dt_emissao", "nu_cpfcnpj_forn", "vl_documento", 
    "ds_razaosocial_comp"
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
    # Converte "nu_cpfcnpj_comp" e "nu_cpfcnpj_forn" para NUMERIC (int ou float)
    if "nu_cpfcnpj_comp" in item and item["nu_cpfcnpj_comp"] is not None and item["nu_cpfcnpj_comp"] != "":
        try:
            item["nu_cpfcnpj_comp"] = int(float(item["nu_cpfcnpj_comp"]))  # Converte para int (NUMERIC)
        except (ValueError, TypeError):
            item["nu_cpfcnpj_comp"] = None  # Se falhar, define como None
    if "nu_cpfcnpj_forn" in item and item["nu_cpfcnpj_forn"] is not None and item["nu_cpfcnpj_forn"] != "":
        try:
            item["nu_cpfcnpj_forn"] = int(float(item["nu_cpfcnpj_forn"]))  # Converte para int (NUMERIC)
        except (ValueError, TypeError):
            item["nu_cpfcnpj_forn"] = None  # Se falhar, define como None
    # Converte "vl_documento" para FLOAT64
    if "vl_documento" in item and item["vl_documento"] is not None and item["vl_documento"] != "":
        try:
            item["vl_documento"] = float(item["vl_documento"])  # Converte para float (FLOAT64)
        except (ValueError, TypeError):
            item["vl_documento"] = None  # Se falhar, define como None
    # Garante que "nu_nf" seja um número (sem aspas)
    if "nu_nf" in item and item["nu_nf"] is not None and item["nu_nf"] != "":
        try:
            item["nu_nf"] = int(float(item["nu_nf"]))  # Tenta converter para int
        except (ValueError, TypeError):
            item["nu_nf"] = None  # Se falhar, define como None
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

# Salvar o novo arquivo CSV com delimitador ;
try:
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=colunas_mantidas, delimiter=';')
        writer.writeheader()  # Escreve o cabeçalho (nomes das colunas)
        writer.writerows(dados_limpos)  # Escreve as linhas de dados
    print(f"Arquivo CSV limpo salvo com sucesso em: {output_file_path}")
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV limpo: {e}")