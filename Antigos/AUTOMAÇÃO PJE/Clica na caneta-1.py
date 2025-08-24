from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configuração do ChromeDriver
service = Service(executable_path=r"C:\chromedriver-win64\chromedriver.exe")
chrome_options = webdriver.ChromeOptions()

# Uso do perfil padrão
chrome_options.add_argument(r"user-data-dir=C:\Users\mario\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument(r"profile-directory=Default")

# Inicializa o driver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Acessa o ChatGPT
    driver.get("https://chat.openai.com/")

    # Espera a página carregar completamente (ajuste conforme necessário)
    time.sleep(5)  # Ajuste esse tempo se necessário para carregar o site

    # Aguarda a interface do ChatGPT estar disponível
    time.sleep(5)
    
    # Localiza a caixa de entrada do chat (ajuste selector se necessário)
    chat_box = driver.find_element(By.CSS_SELECTOR, "textarea")
    
    # Envia a pergunta "Vai chover amanhã?"
    pergunta = "Vai chover amanhã?"
    chat_box.send_keys(pergunta)
    chat_box.send_keys(Keys.RETURN)
    
    # Espera a resposta
    time.sleep(10)  # Ajuste o tempo conforme necessário para a resposta
    
finally:
    # Fecha o navegador
    driver.quit()
