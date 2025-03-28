import subprocess
import time
from tqdm import tqdm
from datetime import datetime

# Caminhos dos scripts
scripts = [
    r"/home/geraldo.junior/Database_mkt/etl/Atualiza_cnae/getAllCnpj.py",
    r"/home/geraldo.junior/Database_mkt/etl/Atualiza_cnae/getDataFromAPI.py",
    r"/home/geraldo.junior/Database_mkt/etl/Atualiza_cnae/updateAllCnae.py",
]

# Define a primeira execução obrigatória (hoje)
primeira_execucao = "28/03/2025"

# Função para executar um script Python
def run_python_script(script_path):
    try:
        print(f"Executando o script: {script_path}")
        cmd = ["python", script_path]
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            print(f"Script {script_path} executado com sucesso.")
        else:
            print(f"Erro ao executar {script_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script {script_path}: {e}")

# Função principal
def run_all_scripts():
    print(f"\nIniciando execução em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for script in tqdm(scripts, desc="Executando scripts", unit="script"):
        run_python_script(script)
    print("Tarefas concluídas.")

# Variável para evitar execução duplicada no mesmo dia
executado_hoje = False

while True:
    agora = datetime.now()
    hoje_str = agora.strftime("%d/%m/%Y")
    hora_str = agora.strftime("%H:%M")

    if (hoje_str == primeira_execucao or agora.day == 28) and hora_str == "16:00" and not executado_hoje:
        run_all_scripts()
        executado_hoje = True

    # Libera a execução novamente no próximo dia
    if hora_str != "00:00":
        executado_hoje = False

    time.sleep(30)
