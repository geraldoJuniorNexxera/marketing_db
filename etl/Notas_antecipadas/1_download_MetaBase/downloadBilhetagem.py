# -*- coding: utf-8 -*-
import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
                print(f"[ERRO] Erro ao deletar {caminho_arquivo}. Razao: {e}")
    else:
        print(f"[AVISO] O caminho {caminho} nao existe.")

def arquivo_foi_baixado(caminho_downloads, extensao=".csv"):
    for arquivo in os.listdir(caminho_downloads):
        if arquivo.endswith(extensao):
            return True
    return False

caminho_downloads = "/home/geraldo.junior/Database_mkt/etl/Downloads"
limpar_pasta(caminho_downloads)

# Configurando o Firefox para execução em modo headless
print("[INFO] Configurando o Firefox para execucao em modo headless...")
firefox_options = Options()
firefox_options.headless = True

# Configurando o perfil do Firefox para downloads automáticos
print("[INFO] Configurando o perfil do Firefox para downloads automaticos...")
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)  # Pasta customizada
profile.set_preference("browser.download.dir", caminho_downloads)
# Corrigido o MIME type para CSV, alinhando com a verificação de extensão
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
profile.set_preference("pdfjs.disabled", True)
profile.update_preferences()

# Inicializando o driver do Firefox
print("[INFO] Inicializando o driver do Firefox...")
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                           firefox_profile=profile,
                           options=firefox_options)
print("[INFO] Driver inicializado com sucesso!")

# Navegação e login
print("[INFO] Acessando a pagina do Metabase...")
driver.get("https://metabase.cloudint.nexxera.com/question/1509-bilhetagem")

# Utilizando explicit wait para aguardar o carregamento do campo de email
wait = WebDriverWait(driver, 20)
email_input = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/div[1]/div[2]/input")
))

print("[INFO] Preenchendo os dados de login...")
email_input.send_keys("geraldo.junior@nexxera.com")
senha_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/div[2]/div[2]/input")
senha_input.send_keys("Joaopaulo@2025")
print("[INFO] Clicando no botao de login...")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/button/div/div").click()

# Aguardando que o login seja processado e que o próximo elemento esteja disponível
wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[1]/div/div/main/div/div/div[2]/main/div[2]/div/div[3]/a")
))

print("[INFO] Navegando para a pagina de download...")
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div/div[2]/main/div[2]/div/div[3]/a").click()

# Aguarda que o botão de download esteja clicável
wait.until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/span/span/div/div/div[3]/div[1]/div/form/button")
))

print("[INFO] Clicando no botao de download...")
driver.find_element(By.XPATH, "/html/body/span/span/div/div/div[3]/div[1]/div/form/button").click()

print("[INFO] Aguardando o download do arquivo...")
while not arquivo_foi_baixado(caminho_downloads):
    print("[INFO] Arquivo ainda nao baixado, aguardando 1 minuto...")
    time.sleep(60)

print("[INFO] Arquivo baixado com sucesso!")
driver.quit()
print("[INFO] Execucao finalizada!")
