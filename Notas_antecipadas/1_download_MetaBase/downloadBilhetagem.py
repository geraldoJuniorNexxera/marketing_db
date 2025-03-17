import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Função para limpar a pasta de downloads
def limpar_pasta(caminho):
    if os.path.exists(caminho):
        for arquivo in os.listdir(caminho):
            caminho_arquivo = os.path.join(caminho, arquivo)
            try:
                if os.path.isfile(caminho_arquivo) or os.path.islink(caminho_arquivo):
                    os.unlink(caminho_arquivo)
                elif os.path.isdir(caminho_arquivo):
                    shutil.rmtree(caminho_arquivo)
            except Exception as e:
                print(f"Erro ao deletar {caminho_arquivo}. Razão: {e}")
    else:
        print(f"O caminho {caminho} não existe.")

# Função para verificar se o arquivo foi baixado
def arquivo_foi_baixado(caminho_downloads, extensao=".xlsx"):
    for arquivo in os.listdir(caminho_downloads):
        if arquivo.endswith(extensao):
            return True
    return False

# Limpa a pasta de downloads antes de iniciar o código
caminho_downloads = r"C:\Users\geraldo.junior\Downloads"
limpar_pasta(caminho_downloads)

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Maximiza a janela do navegador

# Inicializa o WebDriver usando o webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Acessa a URL
url = "https://metabase.cloudint.nexxera.com/question/1509-bilhetagem"
driver.get(url)

# Aguarda alguns segundos para a página carregar
time.sleep(5)  # Ajuste o tempo conforme necessário

# Preenche o campo de e-mail
email_xpath = "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/div[1]/div[2]/input"
email_field = driver.find_element(By.XPATH, email_xpath)
email_field.send_keys("geraldo.junior@nexxera.com")

# Preenche o campo de senha
senha_xpath = "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/div[2]/div[2]/input"
senha_field = driver.find_element(By.XPATH, senha_xpath)
senha_field.send_keys("Joaopaulo@2025")

# Clica no botão de login
botao_login_xpath = "/html/body/div[1]/div/div/main/div/div[2]/div/div[2]/div/form/button/div/div"
botao_login = driver.find_element(By.XPATH, botao_login_xpath)
botao_login.click()

# Aguarda alguns segundos para a página de destino carregar
time.sleep(10)  # Ajuste o tempo conforme necessário

# Clica no ícone da "nuvem"
click_nuvem = "/html/body/div[1]/div/div/main/div/div/div[2]/main/div[2]/div/div[3]/a"
elemento = driver.find_element(By.XPATH, click_nuvem)
elemento.click()
time.sleep(10)

# Clica para baixar arquivo .xlsx
download_xlsx = "/html/body/span/span/div/div/div[3]/div[2]/div/form/button"
elemento = driver.find_element(By.XPATH, download_xlsx)
elemento.click()

# Aguarda o arquivo ser baixado
while not arquivo_foi_baixado(caminho_downloads):
    time.sleep(1)  # Verifica a cada segundo

print("Arquivo baixado com sucesso!")

# Fecha o navegador
driver.quit()