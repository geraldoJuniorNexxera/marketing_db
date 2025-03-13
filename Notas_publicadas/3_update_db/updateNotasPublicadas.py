import time
from tqdm import tqdm
from google.cloud import bigquery
from google.oauth2 import service_account

# Configurações
project_id = 'meta-vc-contabil'
source_dataset_id = 'marketing_db'
table_name = 'notas_publicadas'
json_key_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\credenciais\big_query_key_geraldo-junior.json"
local_csv_path = r"C:\Users\geraldo.junior\Downloads\notas_limpas.csv"

# Autenticação com a chave JSON
credentials = service_account.Credentials.from_service_account_file(json_key_path)
client = bigquery.Client(credentials=credentials, project=project_id)

# Define o dataset e a tabela de destino
table_ref = f"{project_id}.{source_dataset_id}.{table_name}"

# Configura o job de carregamento
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,  # Pula a primeira linha (cabeçalho)
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # Apaga a tabela existente e cria uma nova
    schema=[
        bigquery.SchemaField("ds_razaosocial_forn", "STRING"),
        bigquery.SchemaField("dt_vcto", "DATE"),
        bigquery.SchemaField("nu_nf", "STRING"),
        bigquery.SchemaField("nu_cpfcnpj_comp", "NUMERIC"),
        bigquery.SchemaField("dt_inclusao", "DATE"),
        bigquery.SchemaField("dt_emissao", "DATE"),
        bigquery.SchemaField("nu_cpfcnpj_forn", "NUMERIC"),
        bigquery.SchemaField("vl_documento", "FLOAT64"),
        bigquery.SchemaField("ds_razaosocial_comp", "STRING"),
    ],
    field_delimiter=";",  # Especifica o delimitador (ajuste conforme necessário)
)

# Carrega o arquivo CSV para o BigQuery
with open(local_csv_path, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    # Barra de progresso simulada
    with tqdm(total=100, desc="Carregando dados", unit="%") as pbar:
        while job.state != 'DONE':
            time.sleep(5)
            job.reload()
            pbar.update(10)  # Atualiza a barra de progresso (ajuste conforme necessário)

# Verifica se o carregamento foi bem-sucedido
if job.state == "DONE":
    if job.errors:
        print(f"Erro ao carregar o arquivo CSV: {job.errors}")
    else:
        print(f"Arquivo CSV carregado com sucesso para a tabela {table_ref}.")
        print(f"Total de linhas carregadas: {job.output_rows}")
else:
    print(f"O job não foi concluído. Estado atual: {job.state}")