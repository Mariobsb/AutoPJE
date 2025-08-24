from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os

# Configure o caminho para o perfil principal do Chrome
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=C:\Users\mario\AppData\Local\Google\Chrome\User Data")  # Substitua pelo caminho correto
options.add_argument(r"profile-directory=Default")

webdriver = webdriver.Chrome(options=options)

# Caminho para o WebDriver do Chrome
driver_path = r"C:\chromedriver-win64\chromedriver.exe"  # Substitua pelo caminho correto
service = Service(executable_path=driver_path)

# Inicializa o WebDriver com o serviço configurado e opções
driver = webdriver.Chrome(service=service, options=options)

# Acesse o WhatsApp Web
driver.get('https://web.whatsapp.com/')

# Aguarde o carregamento e autenticação
try:
	# Espera até que o elemento do QR code esteja presente na página
	WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!']")))
	print("QR code carregado. Por favor, escaneie o QR code com seu celular.")
	
	# Aguarda até que o WhatsApp Web esteja completamente carregado
	WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-tab='3']")))
	print("WhatsApp Web carregado com sucesso.")
	
	# Salvar os cookies em um arquivo
	cookies = driver.get_cookies()
	with open("cookies.pkl", "wb") as file:
		pickle.dump(cookies, file)
	print("Cookies salvos com sucesso.")
	
except Exception as e:
	print(f"Erro durante o carregamento do WhatsApp Web: {e}")

# Fecha o navegador
driver.quit()