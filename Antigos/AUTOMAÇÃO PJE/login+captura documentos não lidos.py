from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pygetwindow as gw
import time
from bs4 import BeautifulSoup
import pandas as pd

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
	time.sleep(10)

	# A partir daqui, o navegador permanece aberto para manipulação
	print("Login realizado com sucesso. O navegador permanecerá aberto para manipulação.")
	
	# Abre a nova URL
	driver.get("https://pje.tjdft.jus.br/pje/Painel/painel_usuario/list.seam")
	
	# Adiciona um tempo de espera para garantir que a página esteja carregada
	time.sleep(5)

	# Localiza todos os elementos de tarefa (títulos e quantidades)
	tarefas = driver.find_elements(By.XPATH, "//td[contains(@class, 'rich-tree-node-text ')]")

	# Lista para armazenar os dados das tarefas
	tarefas_dados = []

	# Itera sobre os elementos encontrados e extrai os dados
	for tarefa in tarefas:
		# Localiza o título da tarefa
		titulo = tarefa.find_element(By.XPATH, ".//b").text
		# Localiza a quantidade de tarefas
		quantidade_tarefas = tarefa.find_element(By.XPATH, ".//small").text
		# Obtém o XPath do elemento
		xpath = tarefa.get_attribute("outerHTML")
		
		# Armazena os dados em um dicionário
		tarefa_dado = {
			"titulo": titulo,
			"quantidade_tarefas": quantidade_tarefas,
			"xpath": xpath
		}
		
		# Adiciona o dicionário à lista
		tarefas_dados.append(tarefa_dado)
		
		# Exibe o resultado
		print(f"Título: {titulo}")

	# Função para clicar no link "analisar documentos não lidos" se a quantidade de processos for maior que 1
	def clicar_analisar_documentos_nao_lidos(tarefas_dados):
		for tarefa in tarefas_dados:
			if tarefa["titulo"] == "analisar documentos não lidos" and int(tarefa["quantidade_tarefas"]) > 1:
				# Localiza o elemento pelo XPath e clica nele
				elemento = driver.find_element(By.XPATH, tarefa["xpath"])
				elemento.click()
				print("Clicou no link 'analisar documentos não lidos'")
				break

	# Chama a função para verificar e clicar no link
	clicar_analisar_documentos_nao_lidos(tarefas_dados)

	time.sleep(10)


except Exception as e:
	print(f"An error occurred: {e}")