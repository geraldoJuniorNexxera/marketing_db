import csv
from datetime import datetime

# Caminho do arquivo CSV original
input_file_path = r"C:\Users\geraldo.junior\Downloads\notas.csv"

# Caminho do arquivo CSV de saída
output_file_path = r"C:\Users\geraldo.junior\Downloads\notas_limpas.csv"

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

# Função para garantir que "dt_emissao" esteja no formato DATE (YYYY-MM-DD)
def formatar_dt_emissao(data):
    try:
        # Tenta converter a data para o formato DATE
        data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
        return data_formatada
    except (ValueError, TypeError):
        # Se a conversão falhar, retorna None ou a data original (dependendo da necessidade)
        return None  # Ou retorne data para manter o valor original

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
        # Formata o campo "dt_inclusao" para remover o horário
        if "dt_inclusao" in item_limpo:
            item_limpo["dt_inclusao"] = formatar_data(item_limpo["dt_inclusao"])
        # Formata o campo "dt_emissao" para garantir o formato DATE
        if "dt_emissao" in item_limpo:
            item_limpo["dt_emissao"] = formatar_dt_emissao(item_limpo["dt_emissao"])
        # Converte os valores numéricos
        item_limpo = converter_valores(item_limpo)
        dados_limpos.append(item_limpo)
    return dados_limpos

# Ler o arquivo CSV original
try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Lê o CSV como um dicionário
        dados = list(reader)  # Converte o reader para uma lista de dicionários
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    exit()

# Limpar os dados
dados_limpos = limpar_csv(dados, colunas_mantidas)

# Salvar o novo arquivo CSV
try:
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=colunas_mantidas)
        writer.writeheader()  # Escreve o cabeçalho (nomes das colunas)
        writer.writerows(dados_limpos)  # Escreve as linhas de dados
    print(f"Arquivo CSV limpo salvo com sucesso em: {output_file_path}")
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV limpo: {e}")