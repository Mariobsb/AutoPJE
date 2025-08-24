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

# Configuração do serviço do Chrome
service = Service(executable_path=chrome_driver_path)

# Inicialização do WebDriver com o serviço configurado
options = webdriver.ChromeOptions()

# Configuração para usar o perfil padrão do Chrome
options.add_argument(r"user-data-dir=C:\Users\mario\AppData\Local\Google\Chrome\User Data")
options.add_argument(r"profile-directory=Default")

# Inicializa o WebDriver com o serviço configurado e opções
driver = webdriver.Chrome(service=service, options=options)

try:
    # Maximizar a janela do navegador
    driver.maximize_window()

    # Navegar para o site do PJe do TJDFT
    driver.get("https://pje.tjdft.jus.br/pje/Painel/painel_usuario/list.seam")

    # Aguardar para verificar se a página foi carregada
    time.sleep(5)

    # Aqui você pode adicionar outras interações necessárias, como login ou navegação em painéis específicos.
    # Por exemplo, se precisar clicar em algum botão ou preencher algum campo:
    # campo_usuario = driver.find_element(By.ID, "id_do_campo")
    # campo_usuario.send_keys("seu_usuario")
    # campo_senha = driver.find_element(By.ID, "id_do_campo_senha")
    # campo_senha.send_keys("sua_senha")
    # botao_login = driver.find_element(By.ID, "id_do_botao_login")
    # botao_login.click()

    # Adicione qualquer outra lógica necessária aqui...

    # Capturar a página inteira em PDF
    screenshot_dir = "C:/Users/mario/Documents/MECA/APC/automação SELENIUM"
    os.makedirs(screenshot_dir, exist_ok=True)

    # Adicionando timestamp ao nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(screenshot_dir, f"pje_tjdft_{timestamp}.pdf")
    
    # Configurações para imprimir em PDF
    print_options = {
        'printBackground': True,
        'paperWidth': 8.27,
        'paperHeight': 11.69
    }
    
    # Envia o comando para imprimir a página como PDF
    result = driver.execute_cdp_cmd("Page.printToPDF", print_options)
    pdf_data = base64.b64decode(result['data'])
    
    with open(pdf_path, 'wb') as file:
        file.write(pdf_data)

    print(f"PDF salvo em: {pdf_path}")

finally:
    # Fechar o navegador
    driver.quit()
