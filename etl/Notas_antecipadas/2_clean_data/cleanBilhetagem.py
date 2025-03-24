# -*- coding: utf-8 -*-

import os
import pandas as pd
import csv
from datetime import datetime
import warnings

# Caminho da pasta onde os arquivos .csv estão localizados
pasta_downloads = r"/home/geraldo.junior/Database_mkt/etl/Downloads"

# Caminho do arquivo CSV de saída
output_file_path = r"/home/geraldo.junior/Database_mkt/etl/Downloads/bilhetagem_limpa.csv"

# Colunas que devem ser mantidas
colunas_mantidas = [
    "cd_antecipa", 
    "dt_operacao", 
    "nu_cnpj_forn", 
    "vl_operacao", 
    "hubly_mercantil_cad_emp ? ds_emp", 
    "hubly_mercantil_cad_emp_2 ? ds_emp", 
    "hubly_mercantil_cad_emp_3 ? ds_emp"
]

# Mapeamento dos nomes das colunas para os novos nomes
mapeamento_colunas = {
    "hubly_mercantil_cad_emp ? ds_emp": "ancora",
    "hubly_mercantil_cad_emp_2 ? ds_emp": "fornecedor",
    "hubly_mercantil_cad_emp_3 ? ds_emp": "banco"
}

# Função para formatar datas no formato YYYY-MM-DD
def formatar_data(data):
    if pd.isna(data):
        return None
    if isinstance(data, pd.Timestamp):
        return data.strftime("%Y-%m-%d")
    if isinstance(data, str):
        try:
            return datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            try:
                return datetime.strptime(data, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
            except ValueError:
                return None
    return None

# Função para converter valores numéricos
def converter_valores(item):
    if "nu_cnpj_forn" in item and item["nu_cnpj_forn"] not in [None, ""]:
        try:
            item["nu_cnpj_forn"] = int(float(item["nu_cnpj_forn"]))
        except (ValueError, TypeError) as e:
            print(f"Erro ao converter nu_cnpj_forn: {e}")
            item["nu_cnpj_forn"] = None

    if "vl_operacao" in item and item["vl_operacao"] not in [None, ""]:
        try:
            item["vl_operacao"] = float(item["vl_operacao"])
        except (ValueError, TypeError) as e:
            print(f"Erro ao converter vl_operacao: {e}")
            item["vl_operacao"] = None

    if "cd_antecipa" in item and item["cd_antecipa"] not in [None, ""]:
        try:
            item["cd_antecipa"] = int(float(item["cd_antecipa"]))
        except (ValueError, TypeError) as e:
            print(f"Erro ao converter cd_antecipa: {e}")
            item["cd_antecipa"] = None

    return item

# Função para limpar os dados
def limpar_csv(data, colunas_mantidas):
    dados_limpos = []
    for item in data:
        item_limpo = {coluna: item.get(coluna) for coluna in colunas_mantidas}
        for coluna_data in ["dt_operacao"]:
            if coluna_data in item_limpo:
                item_limpo[coluna_data] = formatar_data(item_limpo[coluna_data])
        item_limpo = converter_valores(item_limpo)
        dados_limpos.append(item_limpo)
    return dados_limpos

# Listar todos os arquivos .csv na pasta de downloads
arquivos_csv = [arquivo for arquivo in os.listdir(pasta_downloads) if arquivo.endswith('.csv')]

# Verificar se há arquivos .csv na pasta
if not arquivos_csv:
    print("Nenhum arquivo .csv encontrado na pasta.")
    exit()

# Ler o primeiro arquivo .csv encontrado
input_file_path = os.path.join(pasta_downloads, arquivos_csv[0])

# Ler o arquivo CSV com delimitador ','
try:
    df = pd.read_csv(input_file_path, delimiter=',', encoding='utf-8')
    dados = df.to_dict('records')
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    exit()

# Limpar os dados
dados_limpos = limpar_csv(dados, colunas_mantidas)

# Renomear as colunas ao salvar o arquivo CSV
colunas_renomeadas = [mapeamento_colunas.get(coluna, coluna) for coluna in colunas_mantidas]

# Salvar o novo arquivo CSV com delimitador ';'
try:
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=colunas_renomeadas, delimiter=';')
        writer.writeheader()
        for item in dados_limpos:
            item_renomeado = {mapeamento_colunas.get(coluna, coluna): valor for coluna, valor in item.items()}
            writer.writerow(item_renomeado)
    print(f"Arquivo CSV limpo salvo com sucesso em: {output_file_path}")
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV limpo: {e}")
