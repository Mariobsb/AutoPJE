import pygetwindow as gw
import pyautogui
from pywinauto import Application
import logging

# Configuração do logging
logging.basicConfig(filename='execucao_programa.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def localizar_id_janelas_windows():
    """Localiza e imprime os títulos de todas as janelas abertas no Windows."""
    windows = gw.getAllTitles()
    for window in windows:
        logging.info(f"Nome do programa: \"{window}\"")
    return windows

def localizar_abas_janelas_chrome():
    """Localiza e imprime os títulos de todas as abas e janelas do Google Chrome."""
    windows = gw.getAllTitles()
    if 'Google Chrome' in windows:
        chrome_window = gw.getWindowsWithTitle('Google Chrome')[0]
        chrome_window.activate()
        tabs = pyautogui.getWindowsWithTitle('Google Chrome')
        for tab in tabs:
            logging.info(f"Nome do programa: \"{tab.title}\"")
    else:
        logging.info("Google Chrome não está aberto.")

def localizar_elementos_microsoft_teams():
    """Localiza e imprime os elementos do Microsoft Teams usando pywinauto."""
    try:
        app = Application(backend="uia").connect(path="Teams.exe")
        teams_window = app.window(title_re=".*Microsoft Teams.*")
        teams_window.print_control_identifiers()
        logging.info("Elementos do Microsoft Teams localizados com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao localizar elementos do Microsoft Teams: {e}")

def localizar_abas_janelas_firefox():
    """Localiza e imprime os títulos de todas as abas e janelas do Mozilla Firefox."""
    windows = gw.getAllTitles()
    if 'Mozilla Firefox' in windows:
        firefox_window = gw.getWindowsWithTitle('Mozilla Firefox')[0]
        firefox_window.activate()
        tabs = pyautogui.getWindowsWithTitle('Mozilla Firefox')
        for tab in tabs:
            logging.info(f"Nome do programa: \"{tab.title}\"")
    else:
        logging.info("Mozilla Firefox não está aberto.")

# Exemplo de uso das funções
if __name__ == "__main__":
    localizar_id_janelas_windows()
    localizar_abas_janelas_chrome()
    localizar_elementos_microsoft_teams()
    localizar_abas_janelas_firefox()