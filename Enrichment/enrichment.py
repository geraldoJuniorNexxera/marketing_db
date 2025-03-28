import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Caminho da pasta onde estão os arquivos e onde o resultado será salvo
caminho_pasta = r"C:\Users\geraldo.junior\Downloads"
caminho_credenciais = r"C:\Users\geraldo.junior\DEV\Database_mkt\credenciais\big_query_key_geraldo-junior.json"

# Lista de extensões suportadas
extensoes_suportadas = ['.xls', '.xlsx', '.csv']

# Lista para armazenar todos os CNPJs lidos
cnpjs_encontrados = []

# Função para ler arquivos e extrair CNPJs da primeira coluna (ignorando a 1ª linha)
def extrair_cnpjs():
    for arquivo in os.listdir(caminho_pasta):
        nome_arquivo, extensao = os.path.splitext(arquivo)

        if extensao.lower() in extensoes_suportadas:
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            try:
                if extensao == '.csv':
                    df = pd.read_csv(caminho_arquivo, encoding='utf-8', sep=';', skiprows=1)
                else:
                    df = pd.read_excel(caminho_arquivo, engine='openpyxl' if extensao == '.xlsx' else 'xlrd', skiprows=1)
                
                # Extrai os CNPJs da primeira coluna e limpa
                cnpjs = df.iloc[:, 0].astype(str).str.replace(r'\D', '', regex=True)
                cnpjs_encontrados.extend(cnpjs.tolist())
                print(f"✅ CNPJs extraídos do arquivo: {arquivo}")

            except Exception as e:
                print(f"❌ Erro ao abrir o arquivo {arquivo}: {e}")

# Função para consultar o BigQuery com os CNPJs lidos
def consultar_bigquery(cnpjs):
    credentials = service_account.Credentials.from_service_account_file(caminho_credenciais)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # Filtra apenas CNPJs válidos com 14 dígitos
    cnpjs_validos = [cnpj for cnpj in cnpjs if cnpj.isdigit() and len(cnpj) == 14]

    if not cnpjs_validos:
        print("⚠️ Nenhum CNPJ válido com 14 dígitos encontrado.")
        return pd.DataFrame(columns=[
            'cnpj', 'razao_social', 'grupo_material', 'material',
            'cnae_principal', 'municipio', 'uf', 'data_abertura', 'porte',
            'faturamento', 'quadro_funcionarios', 'cnae_segmento'
        ])

    # Prepara a lista de CNPJs como subquery no SQL
    cnpjs_formatados = ', '.join(f"'{cnpj}'" for cnpj in cnpjs_validos)

    query = f"""
        WITH cnpjs AS (
            SELECT cnpj FROM UNNEST([{cnpjs_formatados}]) AS cnpj
        )
        SELECT 
            c.cnpj,
            COALESCE(api.razao_social, '--') AS razao_social,
            COALESCE(mc.grupo_material, '--') AS grupo_material,
            COALESCE(mc.material, '--') AS material,
            COALESCE(api.cnae_principal, '--') AS cnae_principal,
            COALESCE(api.municipio, '--') AS municipio,
            COALESCE(api.uf, '--') AS uf,
            COALESCE(CAST(api.data_abertura AS STRING), '--') AS data_abertura,
            COALESCE(api.porte, '--') AS porte,
            COALESCE(api.faturamento, '--') AS faturamento,
            COALESCE(api.quadro_funcionarios, '--') AS quadro_funcionarios,
            COALESCE(api.cnae_segmento, '--') AS cnae_segmento
        FROM cnpjs c
        LEFT JOIN `meta-vc-contabil.marketing_db.Meta_Contabil` mc
            ON c.cnpj = CAST(mc.cnpj AS STRING)
        LEFT JOIN `meta-vc-contabil.marketing_db.Base_Cnae_Api_EmpresaAqui_Limpa` api
            ON c.cnpj = CAST(api.cnpj AS STRING)
    """

    query_job = client.query(query)
    resultados = query_job.result().to_dataframe()

    # Garante que o CNPJ tenha 14 dígitos
    resultados['cnpj'] = resultados['cnpj'].astype(str).str.zfill(14)

    return resultados

# Executa as funções
extrair_cnpjs()

# Normaliza os CNPJs extraídos para 14 dígitos
cnpjs_limpos = [cnpj for cnpj in cnpjs_encontrados if cnpj.isdigit() and len(cnpj) == 14]
df_cnpjs_base = pd.DataFrame({'cnpj': cnpjs_limpos}).drop_duplicates()

if not df_cnpjs_base.empty:
    df_resultado = consultar_bigquery(cnpjs_limpos)

    # Merge com base de origem para garantir todos os CNPJs
    df_final = df_cnpjs_base.merge(df_resultado, on='cnpj', how='left')

    # Remove linhas totalmente duplicadas
    df_final = df_final.drop_duplicates()

    # Exibe e salva resultado
    print("\n🎯 Resultado final da pesquisa:")
    print(df_final)

    caminho_saida = os.path.join(caminho_pasta, "Resultado da pesquisa.xlsx")
    df_final.to_excel(caminho_saida, index=False)
    print(f"\n📁 Resultado salvo em: {caminho_saida}")
else:
    print("⚠️ Nenhum CNPJ válido encontrado para consulta.")
