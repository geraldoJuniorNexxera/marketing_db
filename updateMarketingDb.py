import subprocess
import time
from tqdm import tqdm
import nbformat
from nbconvert import PythonExporter
import schedule

# Caminhos dos scripts
script1_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_publicadas\1_download_MetaBase\downloadNotasPublicadas.py"
script2_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_publicadas\2_clean_data\cleanNotasPublicadas.py"
script3_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_publicadas\3_update_db\updateNotasPublicadas.py"
script4_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_antecipadas\1_download_MetaBase\downloadBilhetagem.py"
script5_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_antecipadas\2_clean_data\cleanBilhetagem.py"
script6_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_antecipadas\3_update_db\updateBilhetagem.py"
script7_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Backup_marketing_db\createBackupDB.ipynb"

scripts = [script1_path, script2_path, script3_path, script4_path, script5_path, script6_path, script7_path]

# Função para executar um script Python
def run_python_script(script_path):
    try:
        print(f"Executando o script: {script_path}")
        result = subprocess.run(["python", script_path], check=True)
        if result.returncode == 0:
            print(f"Script {script_path} executado com sucesso.")
        else:
            print(f"Erro ao executar o script {script_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script {script_path}: {e}")

# Função para executar um Jupyter Notebook
def run_ipynb_notebook(notebook_path):
    try:
        print(f"Executando o notebook: {notebook_path}")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)
        python_exporter = PythonExporter()
        script, _ = python_exporter.from_notebook_node(notebook_content)
        exec(script)
        print(f"Notebook {notebook_path} executado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar o notebook {notebook_path}: {e}")

# Função principal que executa todos os scripts
def run_all_scripts():
    for script in tqdm(scripts, desc="Executando scripts", unit="script"):
        if script.endswith('.ipynb'):
            run_ipynb_notebook(script)
        else:
            run_python_script(script)
    print("Tarefas concluídas: Atualizado tabelas 'notas_publicadas' e 'bilhetagem' e criado Backup do marketing_db.")

# Agenda a execução da função principal
schedule.every().day.at("08:14").do(run_all_scripts)
schedule.every().day.at("13:01").do(run_all_scripts)

# Loop para manter o script rodando e verificar o agendamento
while True:
    schedule.run_pending()
    time.sleep(1)