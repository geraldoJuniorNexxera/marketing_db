# -*- coding: utf-8 -*-
import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

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
    # Verifica se existe arquivo com a extensao esperada (ignorando letras maiusculas e arquivos temporarios)
    for arquivo in os.listdir(caminho_downloads):
        if arquivo.lower().endswith(extensao.lower()) and not arquivo.endswith(".part"):
            return True
    return False

caminho_downloads = "/home/geraldo.junior/Database_mkt/etl/Downloads"
limpar_pasta(caminho_downloads)

# Configurando o Firefox para execucao em modo headless e download automatico
print("[INFO] Configurando o Firefox para execucao em modo headless e download automatico...")
firefox_options = Options()
firefox_options.headless = True
firefox_options.set_preference("browser.download.folderList", 2)  # Pasta customizada
firefox_options.set_preference("browser.download.dir", caminho_downloads)
firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
firefox_options.set_preference("pdfjs.disabled", True)

# Inicializando o driver do Firefox (para Selenium < 4)
print("[INFO] Inicializando o driver do Firefox...")
driver = webdriver.Firefox(
    executable_path=GeckoDriverManager().install(),
    firefox_options=firefox_options
)
print("[INFO] Driver inicializado com sucesso!")

# Navegacao e login
print("[INFO] Acessando a pagina do Metabase...")
driver.get("https://metabase.cloudint.nexxera.com/question/1509-bilhetagem")
time.sleep(5)

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

print("[INFO] Navegando para a pagina de download...")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div/div[2]/main/div[2]/div/div[3]/a")\
      .click()
time.sleep(10)

print("[INFO] Clicando no botao de download...")
driver.find_element(By.XPATH, "/html/body/span/span/div/div/div[3]/div[1]/div/form/button")\
      .click()

print("[INFO] Aguardando o download do arquivo...")
while not arquivo_foi_baixado(caminho_downloads):
    print("[INFO] Arquivo ainda nao baixado, aguardando 1 segundo...")
    time.sleep(1)

print("[INFO] Arquivo baixado com sucesso!")
driver.quit()
print("[INFO] Execucao finalizada!")
