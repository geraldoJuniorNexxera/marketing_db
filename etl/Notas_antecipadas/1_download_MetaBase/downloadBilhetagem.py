# -*- coding: utf-8 -*-
import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define variavel para ignorar proxy local
os.environ["NO_PROXY"] = "localhost,127.0.0.1,localhost.nexxera.com"

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

# Caminho da pasta de downloads
caminho_downloads = "/home/geraldo.junior/Database_mkt/etl/Downloads"
limpar_pasta(caminho_downloads)

# Configuracao do Firefox
print("[INFO] Configurando o Firefox para execucao em modo headless e download automatico...")
firefox_options = Options()
firefox_options.headless = True
firefox_options.binary_location = "/usr/bin/firefox"
firefox_options.set_preference("browser.download.folderList", 2)
firefox_options.set_preference("browser.download.dir", caminho_downloads)
firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
firefox_options.set_preference("pdfjs.disabled", True)
firefox_options.set_preference("network.proxy.type", 0)
firefox_options.set_preference("network.proxy.no_proxies_on", "localhost,127.0.0.1,localhost.nexxera.com")

# Caminho do geckodriver manual
service = Service("/home/geraldo.junior/geckdriver/geckodriver")

# Inicializa o navegador
print("[INFO] Inicializando o driver do Firefox...")
driver = webdriver.Firefox(service=service, options=firefox_options)
print("[INFO] Driver inicializado com sucesso!")

# Acessa o Metabase
print("[INFO] Acessando a pagina do Metabase...")
driver.get("https://metabase.cloudint.nexxera.com/question/1509-bilhetagem")
time.sleep(5)

# Preenche login
print("[INFO] Preenchendo os dados de login...")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/div[1]/div[2]/input")\
      .send_keys("geraldo.junior@nexxera.com")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/div[2]/div[2]/input")\
      .send_keys("Joaopaulo@2025")
print("[INFO] Clicando no botao de login...")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/button/div/div")\
      .click()

print("[INFO] Aguardando 10 segundos para o login processar...")
time.sleep(10)

# Espera o link da pagina de download aparecer e clica com JS
print("[INFO] Aguardando elemento da pagina de download ficar disponivel...")
elemento = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/main/div/div/div[2]/main/div[2]/div/div[3]/a"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
time.sleep(1)
driver.execute_script("arguments[0].click();", elemento)

time.sleep(10)

# Clica no botao de download
print("[INFO] Clicando no botao de download...")
botao_download = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/span/span/div/div/div[3]/div[1]/div/form/button"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", botao_download)
time.sleep(1)
driver.execute_script("arguments[0].click();", botao_download)

# Aguarda o download
print("[INFO] Aguardando o download do arquivo...")
while not arquivo_foi_baixado(caminho_downloads):
    print("[INFO] Arquivo ainda nao baixado, aguardando 60 segundos...")
    time.sleep(60)

print("[INFO] Arquivo baixado com sucesso!")
driver.quit()
print("[INFO] Execucao finalizada!")
