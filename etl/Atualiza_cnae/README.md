############### Rodar código continuamente ################

- Mudar para usuário
    ssh geraldo.junior@flnetl001prd

- Mudar para env
    source /home/geraldo.junior/venv-new/bin/activate

- Rodar o script elt/runAllScripts.py continuamente
    nohup python /home/geraldo.junior/Database_mkt/etl/Atualiza_cnae/runAllScripts.py > log_etl.out 2>&1 &

- Para o script elt/updateMarketingDb_etl.py
    ps aux | grep runAllScripts.py
    geraldo+ 12345  0.1  ... python /home/geraldo.junior/Database_mkt/etl/updateMarketingDb_etl.py
        O número logo após seu nome (neste exemplo, 12345) é o PID do processo
    kill 12345
        ou kill -9 12345