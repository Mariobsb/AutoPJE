from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pygetwindow as gw
import time

# Configuração do WebDriver
chrome_driver_path = r"C:\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
chrome_options = Options()

# Inicializa o WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
	import os
	import time
	import pyautogui
	import pygetwindow as gw
	
	try:
		# Caminho para o atalho do navegador (substitua pelo caminho correto)
		atalho_navegador = r"C:\Users\mario\Favorites\Login PJe.url"
	
		# Abre o atalho do navegador
		os.startfile(atalho_navegador)
	
		# Adiciona um tempo de espera para garantir que o navegador esteja aberto
		time.sleep(5)
	
		# Usa o pyautogui para interagir com a página de login
		# Espera que o iframe esteja disponível e muda para ele
		# Note que a interação com iframes pode ser complexa com pyautogui, então ajuste conforme necessário
		pyautogui.click(x=100, y=200)  # Ajuste as coordenadas conforme necessário
	
		# Espera o elemento estar presente e clicável, e então clica
		pyautogui.click(x=200, y=300)  # Ajuste as coordenadas conforme necessário
	
		# Adiciona um tempo de espera para garantir que a nova janela esteja pronta
		time.sleep(2)
	
		# Foca na janela do PJE Office com o nome "Progresso"
		pje_office_window = gw.getWindowsWithTitle("Progresso")[0]
		pje_office_window.activate()
	
		# Usa o pyautogui para digitar a senha na nova caixa de diálogo
		pyautogui.write('Marior10#')
	
		# Se houver um botão de submit ou algo similar, você pode clicar nele
		pyautogui.press('enter')
	
		# Adiciona um tempo de espera para observar o comportamento do navegador
		time.sleep(20)
	
		# A partir daqui, o navegador permanece aberto para manipulação
		print("Login realizado com sucesso. O navegador permanecerá aberto para manipulação.")
	
	except Exception as e:
		print(f"An error occurred: {e}")
	
	# Removido o bloco finally para que o navegador não seja fechado automaticamente
	
	# Ajusta o tamanho da janela
	driver.set_window_size(1536, 816)
	
	# Espera que o iframe esteja disponível e muda para ele
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe")))
	
	import pyautogui
	import pygetwindow as gw
	import time
	
	# Foca na janela do navegador
	browser_window = gw.getWindowsWithTitle("PJe")[0]
	browser_window.activate()
	
	# Adiciona um tempo de espera para garantir que a página esteja carregada
	time.sleep(5)
	
	# Usa o pyautogui para interagir com a página de login
	# Espera que o iframe esteja disponível e muda para ele
	# Note que a interação com iframes pode ser complexa com pyautogui, então ajuste conforme necessário
	pyautogui.click(x=100, y=200)  # Ajuste as coordenadas conforme necessário
	
	# Espera o elemento estar presente e clicável, e então clica
	pyautogui.click(x=200, y=300)  # Ajuste as coordenadas conforme necessário
	
	# Adiciona um tempo de espera para garantir que a nova janela esteja pronta
	time.sleep(2)
	
	# Foca na janela do PJE Office com o nome "Progresso"
	pje_office_window = gw.getWindowsWithTitle("Progresso")[0]
	pje_office_window.activate()
	
	# Usa o pyautogui para digitar a senha na nova caixa de diálogo
	pyautogui.write('Marior10#')
	
	# Se houver um botão de submit ou algo similar, você pode clicar nele
	pyautogui.press('enter')
	
	# Adiciona um tempo de espera para observar o comportamento do navegador
	time.sleep(20)
	
	# A partir daqui, o navegador permanece aberto para manipulação
	print("Login realizado com sucesso. O navegador permanecerá aberto para manipulação.")

except Exception as e:
	print(f"An error occurred: {e}")

# Removido o bloco finally para que o navegador não seja fechado automaticamente