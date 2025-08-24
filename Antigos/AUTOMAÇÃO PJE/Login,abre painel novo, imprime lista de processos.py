from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import pyautogui
import pygetwindow as gw
import time
from datetime import datetime

def loginpje():
	# Configuração do WebDriver
	chrome_driver_path = r"C:\chromedriver-win64\chromedriver.exe"
	service = Service(executable_path=chrome_driver_path)
	chrome_options = Options()

	# Inicializa o WebDriver
	driver = webdriver.Chrome(service=service, options=chrome_options)

	try:
		# Abre a URL do PJE
		driver.get("https://pje.tjdft.jus.br/pje/login.seam?loginComCertificado=false&cid=36306")

		# Ajusta o tamanho da janela
		driver.set_window_size(1536, 816)

		# Espera que o iframe esteja disponível e muda para ele
		WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe")))

		# Espera o elemento estar presente e clicável, e então clica
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "kc-pje-office"))).click()

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
		time.sleep(3)

		# Abre a página desejada após o login
		driver.get("https://pje.tjdft.jus.br/pje/Painel/painel_usuario/list.seam")

		# Adiciona um tempo de espera para observar o comportamento do navegador
		time.sleep(20)

		# Localiza o elemento pelo XPath
		elemento = driver.find_element(By.XPATH, "/html/body/div[7]/div/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/div[1]")

		# Extrai o texto do elemento
		texto = elemento.text

		# Divide o texto em linhas e colunas (ajuste conforme necessário)
		linhas = texto.split('\n')
		dados = [linha.split('\t') for linha in linhas]

		# Cria um DataFrame do pandas com as colunas especificadas
		df = pd.DataFrame(dados, columns=[''])

		# Gera um nome de arquivo único baseado na data e hora
		nome_arquivo = datetime.now().strftime("tabela_%Y%m%d_%H%M%S.xlsx")

		# Salva o DataFrame em um arquivo Excel
		df.to_excel(nome_arquivo, index=False)

		# Exibe uma mensagem de sucesso
		print(f"Tabela salva com sucesso em {nome_arquivo}")

		# A partir daqui, o navegador permanece aberto para manipulação
		print("Login realizado com sucesso. O navegador permanecerá aberto para manipulação.")

	except Exception as e:
		print(f"An error occurred: {e}")

# Chama a função de login
loginpje()