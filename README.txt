############### Notas_publicadas ###############

Filtros utilizados no link do Metabase "https://metabase.cloudint.nexxera.com/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7InR5cGUiOiJxdWVyeSIsInF1ZXJ5Ijp7InNvdXJjZS10YWJsZSI6NDI2NSwiZmlsdGVyIjpbImFuZCIsWyJ0aW1lLWludGVydmFsIixbImZpZWxkIiw2NDU1MyxudWxsXSwzMDAsImRheSJdLFsiPSIsWyJmaWVsZCIsNjQ1NTEsbnVsbF0sIlMiXSxbIj0iLFsiZmllbGQiLDY0NTU1LG51bGxdLCJOIl1dfSwiZGF0YWJhc2UiOjh9LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0="

- fg_antecipavel = "S"
- fg_antecipado = "N"
- dt_vcto = "Próximos 300 dias"



############### Notas_antecipadas ############### (Antigo)

Filtro utilizado no Link do Metabase: https://metabase.cloudint.nexxera.com/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7InR5cGUiOiJxdWVyeSIsInF1ZXJ5Ijp7InNvdXJjZS10YWJsZSI6NDI2NSwib3JkZXItYnkiOltbImRlc2MiLFsiZmllbGQiLDY0NTUwLG51bGxdXV0sImZpbHRlciI6WyJhbmQiLFsidGltZS1pbnRlcnZhbCIsWyJmaWVsZCIsNjQ1NTMsbnVsbF0sMzAwLCJkYXkiXSxbIj0iLFsiZmllbGQiLDY0NTUxLG51bGxdLCJTIl0sWyI9IixbImZpZWxkIiw2NDU1NSxudWxsXSwiTiJdXX0sImRhdGFiYXNlIjo4fSwiZGlzcGxheSI6InRhYmxlIiwidmlzdWFsaXphdGlvbl9zZXR0aW5ncyI6e319

- dt_vcto = "Próximos 300 dias"
- fg_antecipavel = "S"
- fg_antecipado = "N"



############### Atualizando Database_mkt (via ETL) ###############


- Ativar script:
nohup /usr/bin/python3 /home/geraldo.junior/Database_mkt/updateMarketingDb.py > /home/geraldo.junior/Database_mkt/log_execucao.txt 2>&1 &


- Verificar se script está rodando: 
ps aux | grep updateMarketingDb.py | grep -v grep

- Derrubar script
pkill -f updateMarketingDb.py


############### Acessar geraldo.junior/Database_mkt (via ETL) ###############

- Mudar para usuário
    ssh geraldo.junior@flnetl001prd

- Mudar para env
    source /home/geraldo.junior/venv-new/bin/activate

- Rodar script fingindo que tem dusplay: 
    xvfb-run -a python downloadBilhetagem.py
    xvfb-run -a python downloadNotasPublicadas.py




