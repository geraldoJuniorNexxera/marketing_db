# -*- coding: utf-8 -*-

import os
import csv
from datetime import datetime

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
    "hubly_mercantil_cad_emp â†’ ds_emp", 
    "hubly_mercantil_cad_emp_2 â†’ ds_emp", 
    "hubly_mercantil_cad_emp_3 â†’ ds_emp"
]

# Mapeamento dos nomes das colunas para os novos nomes
mapeamento_colunas = {
    "hubly_mercantil_cad_emp â†’ ds_emp": "ancora",
    "hubly_mercantil_cad_emp_2 â†’ ds_emp": "fornecedor",
    "hubly_mercantil_cad_emp_3 â†’ ds_emp": "banco"
}

# Função para formatar datas no formato YYYY-MM-DD
def formatar_data(data):
    if not data:
        return None
    for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"]:
        try:
            return datetime.strptime(data, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

# Função para converter valores numéricos
def converter_valores(item):
    for campo, tipo in [("nu_cnpj_forn", int), ("vl_operacao", float), ("cd_antecipa", int)]:
        valor = item.get(campo)
        if valor:
            try:
                item[campo] = tipo(float(valor))
            except (ValueError, TypeError):
                print(f"Erro ao converter {campo}: {valor}")
                item[campo] = None
    return item

# Função para limpar os dados
def limpar_csv(data, colunas_mantidas):
    dados_limpos = []
    for item in data:
        item_limpo = {coluna: item.get(coluna, None) for coluna in colunas_mantidas}
        item_limpo["dt_operacao"] = formatar_data(item_limpo.get("dt_operacao"))
        item_limpo = converter_valores(item_limpo)
        dados_limpos.append(item_limpo)
    return dados_limpos

# Listar arquivos .csv na pasta
aquivos_csv = [arq for arq in os.listdir(pasta_downloads) if arq.endswith('.csv')]

if not aquivos_csv:
    print("Nenhum arquivo .csv encontrado na pasta.")
    exit()

# Ler o primeiro arquivo .csv
input_file_path = os.path.join(pasta_downloads, aquivos_csv[0])

try:
    with open(input_file_path, mode='r', encoding='utf-8') as file:
        leitor_csv = csv.DictReader(file, delimiter=',')
        dados = [linha for linha in leitor_csv]
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    exit()

# Limpar os dados
dados_limpos = limpar_csv(dados, colunas_mantidas)

# Renomear colunas para escrita
colunas_renomeadas = [mapeamento_colunas.get(coluna, coluna) for coluna in colunas_mantidas]

# Salvar arquivo CSV limpo com delimitador ';'
try:
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=colunas_renomeadas, delimiter=';')
        writer.writeheader()
        for item in dados_limpos:
            item_renomeado = {mapeamento_colunas.get(k, k): v for k, v in item.items()}
            writer.writerow(item_renomeado)
    print(f"Arquivo CSV limpo salvo com sucesso em: {output_file_path}")
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV limpo: {e}")
