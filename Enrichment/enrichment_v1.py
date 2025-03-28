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
    print("\n🔍 Iniciando extração de CNPJs...")
    for arquivo in os.listdir(caminho_pasta):
        nome_arquivo, extensao = os.path.splitext(arquivo)

        if extensao.lower() in extensoes_suportadas:
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            try:
                print(f"📂 Lendo arquivo: {arquivo}")
                if extensao == '.csv':
                    df = pd.read_csv(caminho_arquivo, encoding='utf-8', sep=';', skiprows=1)
                else:
                    df = pd.read_excel(caminho_arquivo, engine='openpyxl' if extensao == '.xlsx' else 'xlrd', skiprows=1)
                
                # Extrai os CNPJs da primeira coluna e limpa
                cnpjs = df.iloc[:, 0].astype(str).str.replace(r'\D', '', regex=True)
                cnpjs_encontrados.extend(cnpjs.tolist())
                print(f"✅ {len(cnpjs)} CNPJs extraídos de {arquivo}")

            except Exception as e:
                print(f"❌ Erro ao abrir o arquivo {arquivo}: {e}")

# Função para consultar o BigQuery com os CNPJs lidos
def consultar_bigquery(cnpjs):
    credentials = service_account.Credentials.from_service_account_file(caminho_credenciais)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    print(f"\n📋 Total de CNPJs válidos para consulta: {len(cnpjs)}")
    print(f"🧾 Exemplo de CNPJs: {cnpjs[:10]}")

    # Prepara CNPJs com aspas para UNNEST como STRING
    cnpjs_formatados = ', '.join(f"'{cnpj}'" for cnpj in cnpjs)

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

    print("\n📤 Enviando consulta ao BigQuery...")
    query_job = client.query(query)
    resultados = query_job.result().to_dataframe()
    print(f"✅ Consulta finalizada. Registros retornados: {len(resultados)}")

    resultados['cnpj'] = resultados['cnpj'].astype(str).str.zfill(14)

    return resultados

# Executa as funções
extrair_cnpjs()

# Log total bruto
print(f"\n📦 Total bruto de CNPJs extraídos: {len(cnpjs_encontrados)}")

# Normaliza para 14 dígitos com padding à esquerda
cnpjs_validos = []
cnpjs_invalidos = []

for cnpj in cnpjs_encontrados:
    if isinstance(cnpj, str):
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
        if 1 <= len(cnpj_limpo) <= 14:
            cnpj_formatado = cnpj_limpo.zfill(14)
            cnpjs_validos.append(cnpj_formatado)
        else:
            cnpjs_invalidos.append(cnpj)
    else:
        cnpjs_invalidos.append(str(cnpj))

print(f"✔️ CNPJs considerados após padding (1 a 14 dígitos): {len(cnpjs_validos)}")
print(f"❌ CNPJs ignorados (0 dígitos ou inválidos): {len(cnpjs_invalidos)}")

# Salva inválidos para conferência
if cnpjs_invalidos:
    pd.DataFrame({'cnpjs_invalidos': cnpjs_invalidos}).to_excel(
        os.path.join(caminho_pasta, 'CNPJs_Invalidos.xlsx'),
        index=False
    )
    print("📁 CNPJs inválidos salvos em 'CNPJs_Invalidos.xlsx'")

# Remove duplicados
df_cnpjs_base = pd.DataFrame({'cnpj': cnpjs_validos}).drop_duplicates()
print(f"🔁 CNPJs distintos após padronização e remoção de duplicados: {len(df_cnpjs_base)}")

# Executa consulta se houver CNPJs válidos
if not df_cnpjs_base.empty:
    df_resultado = consultar_bigquery(df_cnpjs_base['cnpj'].tolist())

    # Merge com base original para manter todos os CNPJs
    df_final = df_cnpjs_base.merge(df_resultado, on='cnpj', how='left')

    # Remove linhas duplicadas
    df_final = df_final.drop_duplicates()

    print("\n🎯 Resultado final da pesquisa:")
    print(df_final.head())

    caminho_saida = os.path.join(caminho_pasta, "Resultado da pesquisa.xlsx")
    df_final.to_excel(caminho_saida, index=False)
    print(f"\n📁 Resultado salvo em: {caminho_saida}")
else:
    print("⚠️ Nenhum CNPJ válido encontrado para consulta.")
