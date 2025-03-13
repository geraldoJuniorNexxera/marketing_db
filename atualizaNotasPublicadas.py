import subprocess
import time

# Caminhos para os scripts
script1_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_publicadas\1_download_MetaBase\downloadMetaBase.py"
script2_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_publicadas\2_clean_data\cleanNotasPublicadas.py"
script3_path = r"C:\Users\geraldo.junior\DEV\Database_mkt\Notas_publicadas\3_update_db\updateNotasPublicadas.py"

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

# Executa os scripts em sequência
run_script(script1_path)
run_script(script2_path)
run_script(script3_path)

print("Todos os scripts foram executados.")