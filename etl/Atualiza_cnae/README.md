############### Rodar código continuamente ################

- Mudar para usuário
    ssh geraldo.junior@flnetl001prd

- Mudar para env
    source /home/geraldo.junior/venv-new/bin/activate

- Rodar o script elt/runAllScripts.py continuamente
    nohup python /home/geraldo.junior/Database_mkt/etl/Atualiza_cnae/runAllScripts.py > log_etl.out 2>&1 &
