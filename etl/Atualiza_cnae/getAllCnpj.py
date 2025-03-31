import os
import shutil
import csv
from google.cloud import bigquery
from google.oauth2 import service_account

# Diretorio que sera limpo
result_dir = "/home/geraldo.junior/Database_mkt/etl/Atualiza_cnae/resultado"

# Limpa o diretorio: remove todos os arquivos e subpastas
if os.path.exists(result_dir):
    for filename in os.listdir(result_dir):
        file_path = os.path.join(result_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove arquivo ou link simbolico
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove subpasta
        except Exception as e:
            print(f"Nao foi possivel remover {file_path}. Motivo: {e}")

# Caminho da chave de autenticacao do BigQuery
json_key_path = r"/home/geraldo.junior/Database_mkt/credenciais/big_query_key_geraldo-junior.json"

# Caminho de saida do arquivo CSV
output_csv_path = os.path.join(result_dir, "Lista_de_cnpj.csv")

# Criacao das credenciais com a chave de servico
credentials = service_account.Credentials.from_service_account_file(json_key_path)

# Instanciacao do cliente BigQuery
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# Query a ser executada
query = """
SELECT DISTINCT cnpj
FROM (
  SELECT cnpj FROM `meta-vc-contabil.marketing_db.Base_Salesforce`
  UNION ALL
  SELECT cnpj FROM `meta-vc-contabil.marketing_db.Base_Spokes_Comunidades`
  UNION ALL
  SELECT cnpj FROM `meta-vc-contabil.marketing_db.Meta_Contabil`
  UNION ALL
  SELECT cnpj_cedente FROM `meta-vc-contabil.marketing_db_etl.notas_publicadas`
  UNION ALL
  SELECT CUSTOMER_DOCUMENT FROM `meta-vc-contabil.marketing_db.Base_minha_nexx`
) AS all_cnpj
"""

# Executa a consulta
query_job = client.query(query)
results = query_job.result()  # Aguarda os resultados

# Escreve os dados diretamente no arquivo CSV
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['cnpj'])  # Cabecalho
    for row in results:
        writer.writerow([row.cnpj])

print(f"Arquivo CSV salvo com sucesso em: {output_csv_path}")
