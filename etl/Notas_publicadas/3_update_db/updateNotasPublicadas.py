# -*- coding: utf-8 -*-

import time
from tqdm import tqdm
from google.cloud import bigquery
from google.oauth2 import service_account

# Configuracoes
project_id = 'meta-vc-contabil'
source_dataset_id = 'marketing_db_etl'
table_name = 'notas_publicadas'
json_key_path = r"/home/geraldo.junior/Database_mkt/credenciais/big_query_key_geraldo-junior.json"
local_csv_path = r"/home/geraldo.junior/Database_mkt/etl/Downloads/notas_limpas.csv"

# Autenticacao com a chave JSON
credentials = service_account.Credentials.from_service_account_file(json_key_path)
client = bigquery.Client(credentials=credentials, project=project_id)

# Define o dataset e a tabela de destino
table_ref = f"{project_id}.{source_dataset_id}.{table_name}"

# Configura o job de carregamento
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,  # Pula a primeira linha (cabecalho)
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    schema=[
        bigquery.SchemaField("id_nota", "STRING"),
        bigquery.SchemaField("sacado", "STRING"),
        bigquery.SchemaField("vl_documento", "FLOAT64"),
        bigquery.SchemaField("dt_inclusao", "DATE"),
        bigquery.SchemaField("cedente", "STRING"),
        bigquery.SchemaField("cnpj_cedente", "NUMERIC"),
        bigquery.SchemaField("dt_vcto", "DATE"),
        bigquery.SchemaField("dt_emissao", "DATE"),
    ],
    field_delimiter=";",        # delimitador
    encoding="ISO-8859-1",      # <-- Forca a leitura em ISO-8859-1
)

# Carrega o arquivo CSV para o BigQuery
with open(local_csv_path, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    # Barra de progresso simulada
    with tqdm(total=100, desc="Carregando dados", unit="%") as pbar:
        while job.state != 'DONE':
            time.sleep(5)
            job.reload()
            pbar.update(10)

# Verifica se o carregamento foi bem-sucedido
if job.state == "DONE":
    if job.errors:
        print(f"Erro ao carregar o arquivo CSV: {job.errors}")
    else:
        print(f"Arquivo CSV carregado com sucesso para a tabela {table_ref}.")
        print(f"Total de linhas carregadas: {job.output_rows} (Bilhetagem)")
else:
    print(f"O job nao foi concluido. Estado atual: {job.state}")
