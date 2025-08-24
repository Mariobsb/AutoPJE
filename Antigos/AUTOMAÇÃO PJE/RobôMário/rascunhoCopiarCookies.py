from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import json

# Caminho para o chromedriver
chrome_driver_path = 'C:/chromedriver-win64/chromedriver.exe'
assert os.path.exists(chrome_driver_path), "ChromeDriver path is incorrect"

# Configuração do serviço do Chrome
service = Service(executable_path=chrome_driver_path)

# Função para extrair cookies de um perfil existente
def extract_cookies(profile_path, url):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_path}")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)  # Aguarde o carregamento da página
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

# Função para importar cookies para um perfil temporário
def import_cookies(cookies, url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)  # Aguarde o carregamento da página
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()  # Recarregar a página para aplicar os cookies
    time.sleep(5)  # Aguarde o carregamento da página
    return driver

# Caminho para o perfil existente
profile_path = r"C:\Users\mario\AppData\Local\Google\Chrome\User Data"
assert os.path.exists(profile_path), "Profile directory path is incorrect"

# URL do site para o qual você deseja importar os cookies
url = "https://www.example.com"

# Extrair cookies do perfil existente
cookies = extract_cookies(profile_path, url)

# Salvar cookies em um arquivo (opcional)
with open("cookies.json", "w") as file:
    json.dump(cookies, file)

# Importar cookies para um perfil temporário
driver = import_cookies(cookies, url)

try:
    # Agora você pode continuar a automação com o perfil temporário e os cookies importados
    # Exemplo: Navegar para o Google
    driver.get("https://www.google.com")
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

finally:
    # Fechar o navegador
    driver.quit()