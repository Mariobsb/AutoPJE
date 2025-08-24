from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pygetwindow as gw
import time
import funções

# Exemplo de uso da função login_pje
if __name__ == "__main__":
    # Configuração do WebDriver
    chrome_driver_path = r"C:\chromedriver-win64\chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)
    chrome_options = Options()

    # Inicializa o WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Chama a função de login
    funções.login_pje(driver)

    funções.abre_novopainel(driver)

    funções.abre_publicar_DJE(driver)