======================= Notas_publicadas =======================

Filtros utilizados no link do Metabase "https://metabase.cloudint.nexxera.com/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7InR5cGUiOiJxdWVyeSIsInF1ZXJ5Ijp7InNvdXJjZS10YWJsZSI6NDI2NSwiZmlsdGVyIjpbImFuZCIsWyJ0aW1lLWludGVydmFsIixbImZpZWxkIiw2NDU1MyxudWxsXSwzMDAsImRheSJdLFsiPSIsWyJmaWVsZCIsNjQ1NTEsbnVsbF0sIlMiXSxbIj0iLFsiZmllbGQiLDY0NTU1LG51bGxdLCJOIl1dfSwiZGF0YWJhc2UiOjh9LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0="

- fg_antecipavel = "S"
- fg_antecipado = "N"
- dt_vcto = "Próximos 300 dias"

======================= Notas_antecipadas ======================= 
Filtro utilizado no Link do Metabase: "https://metabase.cloudint.nexxera.com/question/1509-bilhetagem"

- dt_vcto = "Próximos 300 dias"
- fg_antecipavel = "S"
- fg_antecipado = "N"

======================= Acessar geraldo.junior/Database_mkt (via ETL) =======================

- Mudar para usuário
    ssh geraldo.junior@flnetl001prd

- Mudar para env
    source /home/geraldo.junior/venv-new/bin/activate

- Rodar script fingindo que tem dusplay: 
    xvfb-run -a python downloadBilhetagem.py
    xvfb-run -a python downloadNotasPublicadas.py

- Rodar o script elt/updateMarketingDb_etl.py continuamente
    nohup python /home/geraldo.junior/Database_mkt/etl/updateMarketingDb_etl.py > log_etl.out 2>&1 &

- Para o script elt/updateMarketingDb_etl.py
    ps aux | grep updateMarketingDb_etl.py
    geraldo+ 12345  0.1  ... python /home/geraldo.junior/Database_mkt/etl/updateMarketingDb_etl.py
        O número logo após seu nome (neste exemplo, 12345) é o PID do processo
    kill 12345
        ou kill -9 12345



