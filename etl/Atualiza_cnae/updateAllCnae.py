# -*- coding: utf-8 -*-

import time
from tqdm import tqdm
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# Configuracoes
project_id = 'meta-vc-contabil'
source_dataset_id = 'marketing_db_etl'
table_base_name = 'base_cnae'
json_key_path = r"/home/geraldo.junior/Database_mkt/credenciais/big_query_key_geraldo-junior.json"
local_csv_path = r"/home/geraldo.junior/Database_mkt/etl/Atualiza_cnae/resultado/Arquivo_para_upload_Big_query.csv"

# Data atual no formato DD_MM_YYYY
data_atual = datetime.today().strftime("%d_%m_%Y")
table_name = f"{table_base_name}_{data_atual}"
table_id = f"{project_id}.{source_dataset_id}.{table_name}"

# Autenticacao com a chave JSON
credentials = service_account.Credentials.from_service_account_file(json_key_path)
client = bigquery.Client(credentials=credentials, project=project_id)

# Define o schema da tabela conforme solicitado
schema = [
    bigquery.SchemaField("cnpj", "NUMERIC", mode="NULLABLE", precision=14, scale=0),
    bigquery.SchemaField("descricao_identificador_matriz_filial", "STRING"),
    bigquery.SchemaField("nome_fantasia", "STRING"),
    bigquery.SchemaField("descricao_situacao_cadastral", "STRING"),
    bigquery.SchemaField("data_situacao_cadastral", "DATE"),
    bigquery.SchemaField("descricao_motivo_situacao_cadastral", "STRING"),
    bigquery.SchemaField("cnae_fiscal", "NUMERIC"),
    bigquery.SchemaField("cnae_fiscal_descricao", "STRING"),
    bigquery.SchemaField("uf", "STRING"),
    bigquery.SchemaField("municipio", "STRING"),
    bigquery.SchemaField("razao_social", "STRING"),
    bigquery.SchemaField("porte", "STRING"),
]

# Cria a tabela no BigQuery (substitui se ja existir)
table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table, exists_ok=True)
print(f"Tabela criada: {table_id}")

# Configuracao do job de carga
job_config = bigquery.LoadJobConfig(
    schema=schema,
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,           # <<< Ignora a primeira linha do CSV
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    field_delimiter=";"            # <<< Define delimitador como ponto e virgula
)

# Carrega o arquivo CSV para o BigQuery
with open(local_csv_path, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    # Barra de progresso simulada
    with tqdm(total=100, desc="Carregando dados", unit="%") as pbar:
        while job.state != 'DONE':
            time.sleep(5)
            job.reload()
            pbar.update(10)

# Verifica o resultado
if job.state == "DONE":
    if job.errors:
        print(f"Erro ao carregar o arquivo CSV: {job.errors}")
    else:
        print(f"Arquivo CSV carregado com sucesso para a tabela {table_id}.")
        print(f"Total de linhas carregadas: {job.output_rows}")
else:
    print(f"O job nao foi concluido. Estado atual: {job.state}")
