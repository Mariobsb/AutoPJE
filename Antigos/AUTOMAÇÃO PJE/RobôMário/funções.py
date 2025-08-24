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
import os

def login_pje(driver):
    try:
        pass
    except:
        pass
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


def abre_analisar_docs_nao_lidos(driver):
    try:
        print("Tentando acessar o iframe...")
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="ngFrame"]')))
        print("Iframe acessado com sucesso.")
        
        print("Tentando encontrar o elemento para clicar...")
        elemento = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/selector/div/div/div[2]/right-panel/div/div/div[3]/tarefas/div/div[4]/div[25]/div/a/div/span[1]')))
        print("Elemento encontrado. Realizando clique...")
        elemento.click()
        print("Clique realizado com sucesso.")
        time.sleep(20)
    except Exception as e:
        print(f"Não há documentos não lidos para análise ou ocorreu um erro: {e}")

#CÓDIGO PARA ABRIR TAREFA PUBLICAR DJE
3/html/body/app-root/selector/div/div/div[2]/right-panel/div/div/div[3]/tarefas/div/div[4]/div[54]/div/a/div/span[1]
def abre_publicar_DJE(driver):
        try:
            print("Tentando acessar o iframe...")
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="ngFrame"]')))
            print("Iframe acessado com sucesso.")
            
            print("Tentando encontrar o elemento para clicar...")
            elemento = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/selector/div/div/div[2]/right-panel/div/div/div[3]/tarefas/div/div[4]/div[54]/div/a/div/span[1]')))
            print("Elemento encontrado. Realizando clique...")
            elemento.click()
            print("Clique realizado com sucesso.")
            time.sleep(20)
        except Exception as e:
            print(f"Não há documentos não lidos para análise ou ocorreu um erro: {e}")
    except Exception as e:
        print(f"Não há documentos não lidos para análise ou ocorreu um erro: {e}")


def abre_novopainel(driver):
    try:
        driver.maximize_window()
        driver.get("https://pje.tjdft.jus.br/pje/ng2/dev.seam#/painel-usuario-interno")

    except Exception as e:
        print(f"erro ao abrir o novo painel - usuário interno: {e}")

def abre_analisar_docs_nao_lidos_link(driver):
    try:
        driver.get("https://pje-frontend.tjdft.jus.br/#/painel-usuario-interno/lista-processos-tarefa/Analisar%20documentos%20n%C3%A3o%20lidos%20%5BDOCS%5D/eyJtb2RvQ29tcGxldG8iOmZhbHNlLCJudW1lcm9Qcm9jZXNzbyI6IiIsIm51bWVyb1Byb2Nlc3NvUmVmZXJlbmNpYSI6IiIsImNvbXBldGVuY2lhIjoiIiwiZmlsdHJhclBvckRhdGEiOm51bGwsImRhdGFJbmljaW8iOm51bGwsImRhdGFGaW0iOm51bGwsInZhbG9yTWFpb3JRdWUiOm51bGwsInZhbG9yTWVub3JRdWUiOm51bGwsIm5pdmVsU2lnaWxvIjpudWxsLCJmaWx0cm9QcmVmZXJlbmNpYWwiOmZhbHNlLCJldGlxdWV0YXMiOltdLCJvcmRlbmFyU2VtUHJpb3JpZGFkZSI6ZmFsc2V9")
    except Exception as e:
        print(f"erro ao abrir link: {e}")


def clicar_em_processos1(driver):
    # Aguarde até que a lista de processos esteja presente na página
    processos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//ul/li/processo-datalist-card/div/div[3]/a/div/span[2]"))
    )
    
    # Imprimir a relação de processos
    print("Relação de Processos:")
    for idx, processo in enumerate(processos, start=1):
        print(f"Processo {idx}: {processo.text}")
    
    # Realizar o clique no primeiro processo e aguardar 5 minutos
    if processos:
        try:
            # Clique no primeiro processo
            processos[0].click()
            print("Clique realizado no primeiro processo.")

            # Aguarde 5 minutos (300 segundos)
            time.sleep(300)
        except Exception as e:
            print(f"Erro ao clicar no primeiro processo: {e}")
    else:
        print("Nenhum processo encontrado para clicar.")

def clicar_em_processos2(driver):  # Add driver as an argument
    # Maximiza a janela do navegador
    driver.maximize_window()
    
    # Aguarde até que a lista de processos esteja presente na página
    processos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//ul/li/processo-datalist-card/div/div[3]/a/div/span[2]"))
    )

    for index, processo in enumerate(processos):
        try:
            # Rolar para o processo
            driver.execute_script("arguments[0].scrollIntoView();", processo)

            # Pequeno atraso para garantir que a rolagem seja concluída
            time.sleep(1)

            # Re-obter a lista de processos (necessário devido à rolagem)
            processos = driver.find_elements(By.XPATH, "//ul/li/processo-datalist-card/div/div[3]/a/div/span[2]")

            # Clique no processo
            processos[index].click()
            print(f"Clique realizado no processo {index + 1}.")

            # Aguarde 5 segundos antes de clicar no próximo
            time.sleep(5)
        except Exception as e:
            print(f"Erro ao clicar no processo {index + 1}: {e}")

def clicar_em_processos3(driver):  # Add driver as an argument
    # Aguarde até que a lista de processos esteja presente na página
    processos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//ul/li/processo-datalist-card/div/div[3]/a/div/span[2]"))
    )

    actions = ActionChains(driver)

    for index, processo in enumerate(processos):
        try:
            # Rolar para o processo
            driver.execute_script("arguments[0].scrollIntoView(true);", processo)

            # Pequeno atraso para garantir que a rolagem seja concluída
            time.sleep(1)

            # Re-obter a lista de processos (necessário devido à rolagem)
            processos = driver.find_elements(By.XPATH, "//ul/li/processo-datalist-card/div/div[3]/a/div/span[2]")

            # Usar ActionChains para clicar
            actions.move_to_element(processos[index]).click().perform()
            print(f"Clique realizado no processo {index + 1}.")

            # Aguarde 5 segundos antes de clicar no próximo
            time.sleep(5)
        except Exception as e:
            print(f"Erro ao clicar no processo {index + 1}: {e}")

def obter_e_clicar_primeiro_processo(driver):
    try:
        print("Obtendo a quantidade total de processos na lista...")
        processos = driver.find_elements(By.CSS_SELECTOR, 'li div > span.tarefa-numero-processo')
        total_processos = len(processos)
        print(f"Total de processos encontrados: {total_processos}")

        # Imprimir a lista de processos e seus XPaths
        for i, processo in enumerate(processos):
            processo_xpath = f'//*[@id="processosTarefa"]/p-datalist/div/div/ul/li[{i + 1}]/processo-datalist-card/div/div[3]/a/div/span[2]'
            print(f"Processo {i + 1}: {processo.text}, XPath: {processo_xpath}")

        if total_processos > 0:
            print("Clicando no primeiro processo da lista...")
            # Construir o XPath completo para o primeiro processo
            primeiro_processo_xpath = '//*[@id="processosTarefa"]/p-datalist/div/div/ul/li[1]/processo-datalist-card/div/div[3]/a/div/span[2]'
            primeiro_processo = driver.find_element(By.XPATH, primeiro_processo_xpath)
            primeiro_processo.click()
            print("Clique no primeiro processo realizado com sucesso.")
        else:
            print("Nenhum processo encontrado na lista.")
            time.sleep(5)

        return total_processos

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
def copia_texto_docnlido(driver):
    try:
        print("Tentando encontrar o elemento pdf-viewer...")
        # Localiza o elemento <pdf-viewer>
        pdf_viewer = driver.find_element(By.TAG_NAME, 'pdf-viewer')
        print("Elemento pdf-viewer encontrado.")

        # Simula um clique no visualizador para garantir que está em foco
        print("Clicando no pdf-viewer para focar...")
        pdf_viewer.click()

        # Simula Ctrl + A para selecionar todo o texto no visualizador
        print("Selecionando todo o texto no pdf-viewer...")
        pdf_viewer.send_keys(Keys.CONTROL, 'a')
        print("Texto selecionado.")

        # Simula Ctrl + C para copiar o texto selecionado para a área de transferência
        print("Copiando o texto selecionado...")
        pdf_viewer.send_keys(Keys.CONTROL, 'c')
        print("Texto copiado para a área de transferência.")

        # Aguarda um momento para garantir que o texto foi copiado
        print("Aguardando um momento para garantir que o texto foi copiado...")
        time.sleep(1)

        # Usa pyperclip para obter o texto copiado da área de transferência
        print("Tentando obter o texto copiado da área de transferência...")
        texto_copiado = pyperclip.paste()
        print("Texto copiado obtido com sucesso.")
        print("Texto copiado:")
        print(texto_copiado)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")