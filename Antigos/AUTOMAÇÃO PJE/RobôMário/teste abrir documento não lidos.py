import os
from grpc import services
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import pygetwindow as gw  # Corrected import
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip

def login_pje(driver):
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
        password = os.getenv('PJE_PASSWORD')
        if not password:
            raise ValueError("Password not found in environment variables")
        pyautogui.write(password)
        
        # Se houver um botão de submit ou algo similar, você pode clicar nele
        pyautogui.press('enter')

        # Adiciona um tempo de espera para observar o comportamento do navegador
        time.sleep(5)

        print("Login realizado com sucesso. O navegador permanecerá aberto para manipulação.")
        
    except Exception as e:
        print(f"An error occurred during login: {e}")