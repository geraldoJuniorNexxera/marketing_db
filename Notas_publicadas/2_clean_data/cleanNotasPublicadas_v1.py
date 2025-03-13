import json
import os
from datetime import datetime

# Caminho do arquivo JSON original
input_file_path = r"C:\Users\geraldo.junior\Downloads\notas.json"

# Caminho do arquivo JSON de saída
output_file_path = r"C:\Users\geraldo.junior\Downloads\notas_limpas.json"

# Colunas que devem ser mantidas
colunas_mantidas = [
    "ds_razaosocial_forn", "dt_vcto", "nu_nf", "nu_cpfcnpj_comp", 
    "dt_inclusao", "dt_emissao", "nu_cpfcnpj_forn", "vl_documento", 
    "ds_razaosocial_comp"
]

# Função para formatar a data (remover o horário de "dt_inclusao")
def formatar_data(data):
    if data and "T" in data:
        return data.split("T")[0]  # Remove o horário, mantendo apenas a data
    return data

# Função para limpar o JSON
def limpar_json(data, colunas_mantidas):
    dados_limpos = []
    for item in data:
        item_limpo = {coluna: item.get(coluna) for coluna in colunas_mantidas}
        # Formata o campo "dt_inclusao" para remover o horário
        if "dt_inclusao" in item_limpo:
            item_limpo["dt_inclusao"] = formatar_data(item_limpo["dt_inclusao"])
        dados_limpos.append(item_limpo)
    return dados_limpos

# Ler o arquivo JSON original
try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        dados = json.load(file)
except Exception as e:
    print(f"Erro ao ler o arquivo JSON: {e}")
    exit()

# Limpar os dados
dados_limpos = limpar_json(dados, colunas_mantidas)

# Salvar o novo arquivo JSON
try:
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(dados_limpos, file, ensure_ascii=False, indent=4)
    print(f"Arquivo limpo salvo com sucesso em: {output_file_path}")
except Exception as e:
    print(f"Erro ao salvar o arquivo JSON limpo: {e}")