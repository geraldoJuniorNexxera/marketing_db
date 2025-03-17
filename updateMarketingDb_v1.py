import subprocess
import time
from tqdm import tqdm

# Atualiza notas_publicadas
script1_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_publicadas\1_download_MetaBase\downloadNotasPublicadas.py"
script2_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_publicadas\2_clean_data\cleanNotasPublicadas.py"
script3_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_publicadas\3_update_db\updateNotasPublicadas.py"

# Atualiza bilhetagem
script4_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_antecipadas\1_download_MetaBase\downloadBilhetagem.py"
script5_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_antecipadas\2_clean_data\cleanBilhetagem.py"
script6_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_antecipadas\3_update_db\updateBilhetagem.py"

# Cria Backup de todo o "marketing_db"
script7_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Backup_marketing_db\createBackupDB.ipynb"

# Lista de scripts a serem executados
scripts = [script1_path, 
           script2_path, 
           script3_path, 
           script4_path, 
           script5_path, 
           script6_path,
           script7_path
           ]

# Função para executar um script e aguardar sua conclusão
def run_script(script_path):
    try:
        print(f"Executando o script: {script_path}")
        result = subprocess.run(["python", script_path], check=True)
        if result.returncode == 0:
            print(f"Script {script_path} executado com sucesso.")
        else:
            print(f"Erro ao executar o script {script_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script {script_path}: {e}")

# Executa os scripts em sequência com uma barra de loading
for script in tqdm(scripts, desc="Executando scripts", unit="script"):
    run_script(script)

print("As tabelas 'notas_publicadas' e 'bilhetagem' foram atualizadas com sucesso.")