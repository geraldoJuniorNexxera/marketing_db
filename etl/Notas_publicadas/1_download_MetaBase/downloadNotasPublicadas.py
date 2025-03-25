# -*- coding: utf-8 -*-
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def limpar_pasta(caminho):
    print(f"[INFO] Limpando pasta de downloads: {caminho}")
    if os.path.exists(caminho):
        for arquivo in os.listdir(caminho):
            caminho_arquivo = os.path.join(caminho, arquivo)
            try:
                if os.path.isfile(caminho_arquivo) or os.path.islink(caminho_arquivo):
                    os.unlink(caminho_arquivo)
                elif os.path.isdir(caminho_arquivo):
                    shutil.rmtree(caminho_arquivo)
            except Exception as e:
                print(f"[ERRO] Erro ao deletar {caminho_arquivo}. Razo: {e}")
    else:
        print(f"[AVISO] O caminho {caminho} nao existe.")

def arquivo_foi_baixado(caminho_downloads, extensao=".csv"):
    for arquivo in os.listdir(caminho_downloads):
        if arquivo.lower().endswith(extensao.lower()) and not arquivo.endswith(".part"):
            return True
    return False

# Caminhos personalizados
chrome_binary = "/home/geraldo.junior/chrome/opt/google/chrome/google-chrome"
lib_path = "/home/geraldo.junior/libs/usr/lib64"
caminho_downloads = "/home/geraldo.junior/Database_mkt/etl/Downloads"

limpar_pasta(caminho_downloads)

# Configurando Chrome headless
print("[INFO] Configurando o Chrome para execucao headless e download automatico...")
options = Options()
options.binary_location = chrome_binary
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

# Download sem prompt
prefs = {
    "download.default_directory": caminho_downloads,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# Inicializando o ChromeDriver
print("[INFO] Inicializando o ChromeDriver...")
service = Service(ChromeDriverManager().install())
env = os.environ.copy()
env["LD_LIBRARY_PATH"] = lib_path

driver = webdriver.Chrome(service=service, options=options)

# Acesso ao Metabase
print("[INFO] Acessando a pagina do Metabase...")
driver.get("https://metabase.cloudint.nexxera.com/question/1509-bilhetagem")
time.sleep(5)

print("[INFO] Realizando login...")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/div[1]/div[2]/input")\
    .send_keys("geraldo.junior@nexxera.com")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/div[2]/div[2]/input")\
    .send_keys("Joaopaulo@2025")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/button/div/div")\
    .click()

time.sleep(10)

print("[INFO] Navegando para a aba de download...")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div/div[2]/main/div[2]/div/div[3]/a")\
    .click()
time.sleep(10)

print("[INFO] Clicando no botao de download...")
driver.find_element(By.XPATH, "/html/body/span/span/div/div/div[3]/div[1]/div/form/button")\
    .click()

print("[INFO] Aguardando o download...")
while not arquivo_foi_baixado(caminho_downloads):
    print("[INFO] Ainda aguardando... tentando novamente em 60 segundos.")
    time.sleep(60)

print("[INFO] Arquivo baixado com sucesso!")
driver.quit()
print("[INFO] Execucao finalizada!")
