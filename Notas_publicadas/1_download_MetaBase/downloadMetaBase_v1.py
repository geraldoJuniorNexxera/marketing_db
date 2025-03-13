from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Maximiza a janela do navegador

# Inicializa o WebDriver usando o webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Acessa a URL
url = "https://metabase.cloudint.nexxera.com/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7InR5cGUiOiJxdWVyeSIsInF1ZXJ5Ijp7InNvdXJjZS10YWJsZSI6MzgzNSwiZmlsdGVyIjpbImFuZCIsWyI9IixbImZpZWxkIiw1OTIxMyxudWxsXSwiUyJdLFsidGltZS1pbnRlcnZhbCIsWyJmaWVsZCIsNTkyMjgsbnVsbF0sMTUsImRheSJdXX0sImRhdGFiYXNlIjo4fSwiZGlzcGxheSI6InRhYmxlIiwidmlzdWFsaXphdGlvbl9zZXR0aW5ncyI6e319"
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

# Aguarda alguns segundos para a ação ser concluída
time.sleep(5)  # Ajuste o tempo conforme necessário

# Fecha o navegador
driver.quit()