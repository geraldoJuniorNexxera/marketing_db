import subprocess
import time
from tqdm import tqdm
import nbformat
from nbconvert import PythonExporter
import schedule

# Caminhos dos scripts
scripts = [
    r"/home/geraldo.junior/Database_mkt/etl/Notas_publicadas/1_download_MetaBase/downloadNotasPublicadas.py",
    r"/home/geraldo.junior/Database_mkt/etl/Notas_publicadas/2_clean_data/cleanNotasPublicadas.py",
    r"/home/geraldo.junior/Database_mkt/etl/Notas_publicadas/3_update_db/updateNotasPublicadas.py",
    r"/home/geraldo.junior/Database_mkt/etl/Notas_antecipadas/1_download_MetaBase/downloadBilhetagem.py",
    r"/home/geraldo.junior/Database_mkt/etl/Notas_antecipadas/2_clean_data/cleanBilhetagem.py",
    r"/home/geraldo.junior/Database_mkt/etl/Notas_antecipadas/3_update_db/updateBilhetagem.py",
]

# Funcao para executar um script Python
def run_python_script(script_path):
    try:
        print(f"Executando o script: {script_path}")
        # Usa xvfb-run apenas para scripts especificos
        if "downloadBilhetagem.py" in script_path or "downloadNotasPublicadas.py" in script_path:
            cmd = ["xvfb-run", "-a", "python", script_path]
        else:
            cmd = ["python", script_path]

        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            print(f"Script {script_path} executado com sucesso.")
        else:
            print(f"Erro ao executar {script_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script {script_path}: {e}")

# Funcao para executar um Jupyter Notebook
def run_ipynb_notebook(notebook_path):
    try:
        print(f"Executando o notebook: {notebook_path}")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)
        python_exporter = PythonExporter()
        script, _ = python_exporter.from_notebook_node(notebook_content)
        exec(script, {})
        print(f"Notebook {notebook_path} executado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar o notebook {notebook_path}: {e}")

# Funcao principal que executa todos os scripts
def run_all_scripts():
    for script in tqdm(scripts, desc="Executando scripts", unit="script"):
        run_ipynb_notebook(script) if script.endswith('.ipynb') else run_python_script(script)
    print("Tarefas concluidas: Atualizado tabelas 'notas_publicadas' e 'bilhetagem'.")

# Agenda a execucao da funcao principal
schedule.every().day.at("08:00").do(run_all_scripts)
schedule.every().day.at("10:00").do(run_all_scripts)
schedule.every().day.at("12:00").do(run_all_scripts)
schedule.every().day.at("15:00").do(run_all_scripts)
schedule.every().day.at("19:00").do(run_all_scripts)

# Loop para manter o script rodando e verificar o agendamento
while True:
    schedule.run_pending()
    time.sleep(1)
