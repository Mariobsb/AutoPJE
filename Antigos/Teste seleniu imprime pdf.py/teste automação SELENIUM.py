from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import base64
from datetime import datetime

# Caminho para o chromedriver
chrome_driver_path = 'C:/chromedriver-win64/chromedriver.exe'
assert os.path.exists(chrome_driver_path), "ChromeDriver path is incorrect"

# Configuração do serviço do Chrome
service = Service(executable_path=chrome_driver_path)

# Inicialização do WebDriver com o serviço configurado
options = webdriver.ChromeOptions()

# Configuração para usar o perfil padrão do Chrome
profile_path = r"C:\Users\mario\AppData\Local\Google\Chrome\User Data"
assert os.path.exists(profile_path), "Profile directory path is incorrect"
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument(r"profile-directory=Default")

# Inicializa o WebDriver com o serviço configurado e opções
driver = webdriver.Chrome(service=service, options=options)

try:
	# Maximizar a janela do navegador
	driver.maximize_window()

	# Navegar para o Google
	driver.get("https://www.google.com")

	# Aguardar para verificar se a página foi carregada
	time.sleep(5)

	# Encontrar a barra de pesquisa e pesquisar o nome completo
	search_box = driver.find_element(By.NAME, "q")
	search_box.send_keys("MÁRIO RODRIGUES OLIVEIRA")
	search_box.send_keys(Keys.RETURN)

	# Aguardar alguns segundos para garantir que os resultados sejam carregados
	time.sleep(3)

	# Encontrar os três primeiros resultados
	results = driver.find_elements(By.XPATH, "//div[@class='g']//h3")[:3]
	links = driver.find_elements(By.XPATH, "//div[@class='g']//a")[:3]
	assert len(results) == 3 and len(links) == 3, "Failed to locate three search results"

	# Imprimir os títulos e links dos três primeiros resultados
	for i in range(len(results)):
		print(f"Resultado {i+1}: {results[i].text}")
		print(f"Link: {links[i].get_attribute('href')}\n")

	# Capturar a página inteira em PDF
	screenshot_dir = "C:/Users/mario/Documents/MECA/APC/automação SELENIUM"
	os.makedirs(screenshot_dir, exist_ok=True)

	# Adicionando timestamp ao nome do arquivo
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	pdf_path = os.path.join(screenshot_dir, f"resultado_pesquisa_{timestamp}.pdf")
	
	# Configurações para imprimir em PDF
	print_options = {
		'printBackground': True,
		'paperWidth': 8.27,
		'paperHeight': 11.69
	}
	
	# Envia o comando para imprimir a página como PDF
	try:
		result = driver.execute_cdp_cmd("Page.printToPDF", print_options)
		pdf_data = base64.b64decode(result['data'])
	except Exception as e:
		print(f"Failed to generate PDF: {e}")
		driver.quit()
		raise
	
	with open(pdf_path, 'wb') as file:
		file.write(pdf_data)

	print(f"PDF salvo em: {pdf_path}")

finally:
	# Fechar o navegador
	driver.quit()