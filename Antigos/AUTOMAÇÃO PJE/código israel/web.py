from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep, time
import itens
from selenium.webdriver.support import expected_conditions as EC
import sopa
from selenium.common.exceptions import (
    NoSuchFrameException, NoSuchElementException, StaleElementReferenceException,
    ElementClickInterceptedException, ElementNotInteractableException,
    UnexpectedAlertPresentException, WebDriverException, SessionNotCreatedException
)
from selenium.webdriver.remote.webelement import WebElement
intervalo_entre_cliques = 2
from selenium.webdriver.chrome.options import Options

options = Options()
# options.headless = True
# driver = Chrome(chrome_options=options)

options.add_experimental_option('prefs', {
    "download.default_directory": r"C:\temp",
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
    "download.open_pdf_in_system_reader": False,
    "profile.default_content_settings.popups": 0
})

driver = Chrome(options=options)
wait = WebDriverWait(driver, 60)
actions = ActionChains(driver)

def abre_pje():
    try:
        driver.get('https://pje1g.trf1.jus.br/pje/login.seam')
    except WebDriverException:
        sleep(7)
        driver.get('https://pje1g.trf1.jus.br/pje/login.seam')
    try:
        troca_frame(itens.frame_login)
        clica(itens.botao_logar_certificado_cnj)
    except:
        aguarda(itens.botao_logar_certificado)
        clica(itens.botao_logar_certificado)
    troca_frame(itens.frame_lotacao)
    aguarda(itens.nome_do_usuario)

def abre_processo(processo_simples):
    soh_aba_painel_usuario = driver.window_handles
    troca_frame(itens.frame_painel_usuario)
    link = driver.find_element(By.XPATH,
        f'//span[contains(text(), "{processo_simples.numero}")]/ancestor::div[2]/preceding-sibling::div[2]//pje-link-autos-digitais//i')
    try:
        clica(link)
    except StaleElementReferenceException:
        abre_processo(processo_simples)
    abas_abertas = driver.window_handles
    while abas_abertas == soh_aba_painel_usuario:
        print('Aguardando abrir guia autos')
        sleep(0.5)
        abas_abertas = driver.window_handles
    driver.switch_to.window(abas_abertas[-1])
    return abas_abertas[0], abas_abertas[-1]

def auto_click(item):
    sleep(0.3)
    if isinstance(item, WebElement):
        elemento = item
    else:
        elemento = localiza(item)
    elemento.click()

def aguarda_desaparecer(item: dict):
    elemento_encontrado = None
    if 'id' in item:
        elemento_encontrado = wait.until(EC.invisibility_of_element_located((By.ID, item["id"])))
    elif 'xpath' in item:
        elemento_encontrado = wait.until(EC.invisibility_of_element_located((By.XPATH, item["xpath"])))
    elif 'linktext' in item:
        elemento_encontrado = wait.until(EC.invisibility_of_element_located((By.LINK_TEXT, item["linktext"])))
    return elemento_encontrado

def aguarda(item, espera=wait):
    if not isinstance(espera, WebDriverWait):
        espera = WebDriverWait(driver, espera)
    elemento_encontrado = None
    if isinstance(item, dict):
        if 'id' in item:
            elemento_encontrado = espera.until(EC.presence_of_element_located((By.ID, item["id"])))
        elif 'xpath' in item:
            try:
                elemento_encontrado = espera.until(EC.presence_of_element_located((By.XPATH, item["xpath"])))
            except UnexpectedAlertPresentException:
                pass
        elif 'linktext' in item:
            elemento_encontrado = espera.until(EC.presence_of_element_located((By.LINK_TEXT, item["linktext"])))
    else:
        if item.id != 'None':
            elemento_encontrado = espera.until(EC.presence_of_element_located((By.ID, item.id)))
        elif item.xpath != 'None':
            elemento_encontrado = espera.until(EC.presence_of_element_located((By.XPATH, item.xpath)))
    return elemento_encontrado

def aguarda_texto_estar_no_elemento(item: dict, texto: str):
    elemento_encontrado = None
    if 'id' in item:
        elemento_encontrado = wait.until(EC.text_to_be_present_in_element((By.ID, item["id"]), texto))
    elif 'xpath' in item:
        elemento_encontrado = wait.until(EC.text_to_be_present_in_element((By.XPATH, item["xpath"]), texto))
    elif 'linktext' in item:
        elemento_encontrado = wait.until(EC.text_to_be_present_in_element((By.LINK_TEXT, item["linktext"]), texto))
    return elemento_encontrado

def aguarda_clica(item, espera=wait):
    elemento_encontrado = 'elemento não encontrado'
    if 'id' in item:
        elemento_encontrado = espera.until(EC.element_to_be_clickable((By.ID, item["id"])))
    elif 'xpath' in item:
        elemento_encontrado = espera.until(EC.element_to_be_clickable((By.XPATH, item["xpath"])))
    elif 'linktext' in item:
        elemento_encontrado = espera.until(EC.element_to_be_clickable((By.LINK_TEXT, item["linktext"])))
    clica(elemento_encontrado)

def aguarda_carregando():
    aguarda(itens.carregando)
    carregando = True
    while carregando:
        try:
            localiza(itens.carregando)
        except NoSuchElementException:
            sleep(0.3)
            return

def clica(item):
    sleep(next(controle_requisicoes))
    if isinstance(item, WebElement):
        elemento = item
    else:
        elemento = localiza(item)
        sleep(1)
    try:
        driver.execute_script("arguments[0].click();", elemento)
    except StaleElementReferenceException:
        if isinstance(elemento, dict):
            elemento = aguarda(item)
            driver.execute_script("arguments[0].click();", elemento)

def clica_no_numero_do_processo(processo):
    sleep(0.1)
    troca_frame(itens.frame_painel_usuario)
    if not isinstance(processo, str):
       elemento = aguarda({'xpath': f'//processo-datalist-card/div/div[3]/a/div/span[2][contains(text(), "{processo.numero}")]'})
    else:
        elemento = aguarda({'xpath': f'//processo-datalist-card/div/div[3]/a/div/span[2][contains(text(), "{processo.numero}")]'})
    driver.execute_script("arguments[0].click();", elemento)
    aguarda(itens.botao_etiqueta)
    titulo = driver.find_element(By.XPATH, '//*[@id="frameTarefas"]/div/div[1]/div[1]/div/div[1]/a').text
    tempo = 90
    while processo.numero not in titulo:
        if tempo < 0:
            tempo -= 1
            sleep(1)
            print(f'Aguardando carregar processo {processo.numero} no frame tarefa.')
            titulo = driver.find_element(By.XPATH, '//*[@id="frameTarefas"]/div/div[1]/div[1]/div/div[1]/a').text
        else:
            clica_no_numero_do_processo(processo)
            titulo = driver.find_element(By.XPATH, '//*[@id="frameTarefas"]/div/div[1]/div[1]/div/div[1]/a').text

def clica_lembrete_existente(processo):
    if tem_lembrete(processo):
        abre = {'xpath': f'//span[contains(text(), "{processo.numero}")]/ancestor::processo-datalist-card//pje-lembretes/button'}
        clica(abre)

def controla_requisicoes():
    ultima_requisicao = time()
    while True:
        diferenca = time() - ultima_requisicao
        ultima_requisicao = time()
        yield intervalo_entre_cliques - diferenca if intervalo_entre_cliques - diferenca > 0 else 0

controle_requisicoes = controla_requisicoes()

def fecha_lembretes():
    continua = True
    while continua:
        try:
            botao_fecha_lembretes = driver.find_element(By.XPATH, '//button[@aria-label="Fechar"]')
            botao_fecha_lembretes.click()
        except (StaleElementReferenceException, NoSuchElementException):
            continua = False
        except ElementClickInterceptedException:
            sleep(0.5)
        except ElementNotInteractableException:
            sleep(0.5)
            if not botao_fecha_lembretes.is_displayed():
                return

def tem_lembrete(processo):
    botao = driver.find_element(By.XPATH, f'//span[contains(text(), "{processo.numero}")]')
    botao = botao.find_element(By.XPATH, 'ancestor::processo-datalist-card//pje-lembretes/button')
    return True if botao.get_attribute('title') == 'Visualizar lembrete(s)' else False

def leh_lembretes(processo):
    if tem_lembrete(processo):
        clica_lembrete_existente(processo)
        div_lembretes = aguarda(itens.janela_lembretes)
        lista_lembretes = sopa.devolve_lembretes(div_lembretes.get_attribute('innerHTML'))
        fecha_lembretes()
        return lista_lembretes
    else:
        return []

def digita_texto(item, texto):
    if item == itens.campo_pesquisar_etiquetas:
        try:
            campo_recebe_texto = localiza(item)
            campo_recebe_texto.send_keys(texto)
        except ElementNotInteractableException:
            clica(itens.botao_etiqueta)
        return
    campo_recebe_texto = localiza(item)
    campo_recebe_texto.send_keys(texto)

def fechar():
    driver.quit()

def localiza(item: dict):
    if isinstance(item, WebElement):
        return item
    elemento_encontrado = None
    if isinstance(item, dict):
        if "id" in item:
            elemento_encontrado = driver.find_element(By.ID, item["id"])
        elif "xpath" in item:
            elemento_encontrado = driver.find_element(By.XPATH, item["xpath"])
        elif "linktext" in item:
            elemento_encontrado = driver.find_element(By.LINK_TEXT, item["linktext"])
    else:
        if item.id != 'None':
            elemento_encontrado = driver.find_element(By.ID, item.id)
        elif item.xpath != 'None':
            elemento_encontrado = driver.find_element(By.XPATH, item.xpath)
    return elemento_encontrado

def localiza_varios(item):
    lista_elemento_encontrado = None
    if isinstance(item, dict):
        if "id" in item:
            lista_elemento_encontrado = driver.find_elements(By.ID, item["id"])
        elif "xpath" in item:
            lista_elemento_encontrado = driver.find_elements(By.XPATH, item["xpath"])
        elif "linktext" in item:
            lista_elemento_encontrado = driver.find_elements(By.LINK_TEXT, item["linktext"])
    else:
        if item.id != 'None':
            lista_elemento_encontrado = driver.find_elements(By.ID, item.id)
        elif item.xpath != 'None':
            lista_elemento_encontrado = driver.find_elements(By.XPATH, item.xpath)
    return lista_elemento_encontrado

def pega_dados_autos_completo(processo_simples):
    verficia_quantidade_guias_e_fecha()
    aba_painel_usuario, aba_processo_aberto = abre_processo(processo_simples)
    aguarda(itens.timeline)
    tag_body = localiza(itens.body)
    html = tag_body.get_attribute('innerHTML')
    dados_autos_completos = sopa.encontra_dados_autos(html)
    driver.switch_to.window(aba_painel_usuario)
    return dados_autos_completos, aba_processo_aberto, aba_painel_usuario

def troca_frame(frame):
    if frame == itens.frame_lotacao:
        driver.switch_to.default_content()
    elif frame in [itens.frame_painel_usuario, itens.frame_login]:
        driver.switch_to.default_content()
        driver.switch_to.frame(0)
    elif frame == itens.frame_trf1:
        driver.switch_to.default_content()
        driver.switch_to.frame(0)
        driver.switch_to.frame(0)
    elif frame == itens.frame_editor:
        driver.switch_to.default_content()
        driver.switch_to.frame(0)
        driver.switch_to.frame(0)
        frames = 0
        while frames < 1:
            frames = len(driver.find_elements(By.TAG_NAME, 'iframe'))
            sleep(0.1)
            print('Aguardando frame do CKEditor carregar...')
        sleep(0.1)
        driver.switch_to.frame(0)
    elif frame == itens.frame_processo_remetido:
        driver.switch_to.default_content()
        driver.switch_to.frame(0)
        driver.switch_to.frame(0)

def pega_expedientes(aba_processo_aberto, aba_painel_usuario):
    driver.switch_to.window(aba_processo_aberto)
    aguarda_clica(itens.botao_menu_guia_autos)
    aguarda_clica(itens.expedientes)
    aguarda(itens.tabela_expedientes)
    tabela = localiza(itens.tabela_expedientes)
    html = tabela.get_attribute('innerHTML')
    lista_expedientes = sopa.tira_expedientes_da_tabela(html)
    driver.switch_to.window(aba_painel_usuario)
    troca_frame(itens.frame_painel_usuario)
    return lista_expedientes

def verficia_quantidade_guias_e_fecha():
    janelas = driver.window_handles
    if len(janelas) > 1:
        while janelas[-1] != janelas[0]:
            driver.switch_to.window(janelas[-1])
            driver.close()
            driver.switch_to.window(janelas[0])
            janelas = driver.window_handles
        troca_frame(itens.frame_painel_usuario)

def verifica_se_eh_guia_expedientes():
    try:
        driver.find_element(By.XPATH, '//h5[contains(text(), "Expedientes")]')
        return True
    except NoSuchElementException:
        return False

def muda_guia_autos():
    clica(itens.botao_menu_guia_autos)
    aguarda_clica(itens.opcao_autos)
    aguarda(itens.timeline)

def pega_texto_documento(processo, id_documento):
    if id_documento == 'Erro documento não existente':
        print('Erro (id de documento não exite)')
        return 'Erro (id de documento não exite)'
    if verifica_se_eh_guia_expedientes():
        muda_guia_autos()
    texto = 'Erro'
    doc = {'xpath': f"//*[text()[contains(.,'{id_documento}')]]"}
    aguarda_clica(doc)
    sleep(1.5)
    troca_frame(itens.frame_painel_usuario)
    while texto == 'Erro':
        try:
            texto = driver.find_element(By.TAG_NAME, 'body').text
        except:
            pass
    troca_frame(itens.frame_painel_usuario)
    return texto

def pega_texto_ato_judicial():
    texto = 'erro'
    troca_frame(itens.frame_editor)
    continua = True
    while continua:
        try:
            texto = localiza(itens.documento_caixa_avaliar_ato).text
            continua = False
        except:
            pass
    troca_frame(itens.frame_painel_usuario)
    return texto

def pega_texto_minuta():
    sleep(5)
    troca_frame(itens.frame_editor)
    texto = driver.find_element(By.TAG_NAME, 'body').text
    troca_frame(itens.frame_painel_usuario)
    return texto

def anexa_arquivo(file):
    troca_frame(itens.frame_trf1)
    upload_anexo = driver.find_element(By.ID, 'cke_19')
    driver.execute_script("arguments[0].click();", upload_anexo)
    driver.find_element(By.XPATH, "//a[contains(text(),'Adicionar')]")
    troca_frame(itens.frame_painel_usuario)

def limpa_campo(campo_a_ser_limpo):
    localiza(campo_a_ser_limpo).clear()

def etiqueta_nao_estah_marcada(button):
    i = button.find_element(By.TAG_NAME, 'i')
    return True if i.get_attribute('class') == 'far fa-square' else False

def confere_se_eh_guia_lembretes():
    continua = True
    while continua:
        try:
            driver.find_element(By.XPATH, '//h5[contains(text(),"Cadastro de Lembrete")]')
            continua = False
        except NoSuchElementException:
            continue

def abre_guia_lembretes(processo):
    quantidade_guias = len(driver.window_handles)
    if processo.tem_lembrete():
        clica_lembrete_existente(processo)
        aguarda_clica(itens.novo_lembrete)
        troca_frame(itens.frame_painel_usuario)
        fecha_lembretes()
    else:
        button_lembretes = {
            'xpath': f'//span[contains(text(),"{processo.numero}")]/ancestor::div[2]/preceding-sibling::div[@class="row icones"]//pje-lembretes/button'}
        clica(button_lembretes)
    while quantidade_guias == len(driver.window_handles):
        sleep(0.1)
    driver.switch_to.window(driver.window_handles[-1])
    confere_se_eh_guia_lembretes()

def aguarda_visualizacao_do_lembrete_ser_adicionada():
    aguarda(itens.visualizacoes_adicionadas)
    while localiza(itens.visualizacoes_adicionadas).text == '':
        sleep(0.5)

def salva_lembrete():
    clica(itens.adicionar_visualizacao_aba_lembrete)
    aguarda_visualizacao_do_lembrete_ser_adicionada()
    clica(itens.botao_salvar_lembrete)
    aguarda(itens.alert_lembrete_salvo)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    troca_frame(itens.frame_painel_usuario)

def valor_atributo(webelement, atributo):
    valor = webelement.get_attribute(atributo)
    return valor

def verifica_pje_esta_aberto():
    return True if 'pje' in driver.current_url else False

def seleciona_opcao(dropdown, escolha):
    select = Select(dropdown)
    select.select_by_visible_text(escolha)

def abre_pagina_duplicar_processos():
    driver.get('https://pje1g.trf1.jus.br/pje/Processo/ExecutarFluxo/listView.seam')

def aceita_alert():
    alert = driver.switch_to.alert
    alert.accept()

def pega_texto_alerta():
    alert = driver.switch_to.alert
    return alert.text

def aguarda_alert():
    wait.until(EC.alert_is_present())

def pega_lotacao_atual():
    troca_frame(itens.frame_lotacao)
    lotacao = localiza({'xpath': '//*[@id="barraSuperiorPrincipal"]/div/div[2]/ul/li/a/span[1]'})
    resultado = lotacao.get_attribute('data-original-title')
    return resultado

def atualiza_pagina():
    driver.refresh()

def dah_boas_vindas():
    print('Em que posso ajudar?')

def abre_painel_usuario_gestor(opcao):
    acessa_lotacao(opcao)
    __acessa_painel_usuario()

def escolhe_lotacao(dropdown, opcao):
    atual = dropdown.find_element(By.XPATH, 'option[@selected="selected"]').text
    if atual != opcao:
        seleciona_opcao(dropdown, opcao)
        carregando_lotacao = {'xpath': '//*[@id="_viewRoot:status.start"]/div/div[2]/div/div'}
        aguarda(itens.quadro_de_avisos)
        sleep(1)

def __acessa_painel_usuario():
    sleep(0.5)
    clica(itens.botao_menu_esquerdo)
    sleep(0.5)
    clica(itens.opcao_painel)
    sleep(0.5)
    aguarda(itens.opcao_painel_usuario)
    clica(itens.opcao_painel_usuario)
    troca_frame(itens.frame_painel_usuario)
    aguarda(itens.barra_lateral_esquerda)
    dah_boas_vindas()

def acessa_lotacao(opcao):
    if not verifica_pje_esta_aberto():
        abre_pje()
    else:
        troca_frame(itens.frame_lotacao)
    aguarda(itens.nome_do_usuario)
    clica(itens.nome_do_usuario)
    sleep(0.5)
    try:
        clica(itens.lista_lotacao)
    except NoSuchElementException:
        texto = localiza({'xpath': '//*[@id="papeisUsuarioForm"]/div[1]/span[1]'}).text
        return [texto]
    sleep(0.5)
    dropdown = localiza(itens.lista_lotacao)
    if opcao == 'configuracao':
        return [x.text for x in dropdown.find_elements(By.TAG_NAME, 'option')]
    escolhe_lotacao(dropdown, opcao)
    try:
        sleep(0.1)
    except NoSuchElementException:
        pass

def vincula_etiqueta(button):
    sleep(0.8)
    clica(button)
    aguarda_clica(itens.confirma_moveu)
    clica(itens.botao_etiqueta)
    limpa_campo(itens.campo_pesquisar_etiquetas)

def pega_timeline_completa(processo):
    for i in driver.window_handles:
        driver.switch_to.window(i)
        if processo in driver.title:
            if verifica_se_eh_guia_expedientes():
                muda_guia_autos()
            if driver.find_element(By.ID, 'totalPaginas').get_attribute('value') == driver.find_element(By.ID, 'paginaAtual').get_attribute('value'):
                driver.switch_to.window(driver.window_handles[0])
                return
            else:
                while driver.find_element(By.ID, 'totalPaginas').get_attribute('value') != driver.find_element(By.ID, 'paginaAtual').get_attribute('value'):
                    ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.END).key_up(Keys.END).key_up(Keys.CONTROL).perform()
                    sleep(1)
                    try:
                        driver.find_element(By.ID, 'divTimeLine:eventosTimeLineElement').click()
                    except (StaleElementReferenceException, ElementClickInterceptedException):
                        sleep(2)
                        try:
                            driver.find_element(By.ID, 'divTimeLine:eventosTimeLineElement').click()
                        except ElementClickInterceptedException:
                            driver.find_element(By.ID, 'divTimeLine:eventosTimeLineElement').click()
                    aguarda(itens.timeline)
                    tag_body = localiza(itens.body)
                    html = tag_body.get_attribute('innerHTML')
                    dados_autos_completos = sopa.encontra_dados_autos(html)
    driver.switch_to.window(driver.window_handles[0])
    resultado = dados_autos_completos['timeline']
    return resultado

def abre_processo_atos(processo_simples):
    soh_aba_painel_usuario = driver.window_handles
    troca_frame(itens.frame_painel_usuario)
    link = driver.find_element(By.XPATH,
        f'//span[contains(text(), "{processo_simples.numero}")]/ancestor::div[2]/preceding-sibling::div[2]//pje-link-autos-digitais//i')
    try:
        clica(link)
    except StaleElementReferenceException:
        abre_processo(processo_simples)
    abas_abertas = driver.window_handles
    while abas_abertas == soh_aba_painel_usuario:
        print('Aguardando abrir guia autos')
        sleep(0.5)
        abas_abertas = driver.window_handles
    driver.switch_to.window(abas_abertas[1])
    return abas_abertas[1], abas_abertas[-1]

def abre_gpt():
    try:
        driver.execute_script("window.open('https://chatgpt.com/?model=gpt-4o', '_blank')")
        driver.switch_to.window(driver.window_handles[1])
    except WebDriverException:
        sleep(7)
        driver.execute_script("window.open('https://chatgpt.com/?model=gpt-4o', '_blank')")
        driver.switch_to.window(driver.window_handles[1])

def abre_sisbajud():
    try:
        driver.execute_script("window.open('https://sisbajud.cnj.jus.br/minuta', '_blank')")
        driver.switch_to.window(driver.window_handles[1])
    except WebDriverException:
        sleep(7)
        driver.execute_script("window.open('https://sisbajud.cnj.jus.br/minuta', '_blank')")
        driver.switch_to.window(driver.window_handles[1])

def abre_trf1():
    try:
        driver.execute_script("window.open('https://www.trf1.jus.br/sjro/home/', '_blank')")
        driver.switch_to.window(driver.window_handles[1])
    except WebDriverException:
        sleep(7)
        driver.execute_script("window.open('https://www.trf1.jus.br/sjro/home/', '_blank')")
        driver.switch_to.window(driver.window_handles[1])

def abre_renajud():
    try:
        driver.execute_script("window.open('https://renajud.denatran.serpro.gov.br/renajud/login.jsf', '_blank')")
        driver.switch_to.window(driver.window_handles[1])
    except WebDriverException:
        sleep(7)
        driver.execute_script("window.open('https://renajud.denatran.serpro.gov.br/renajud/login.jsf', '_blank')")
        driver.switch_to.window(driver.window_handles[1])

def abre_infojud():
    try:
        driver.execute_script("window.open('https://sso.acesso.gov.br/login?client_id=cav.receita.fazenda.gov.br', '_blank')")
        driver.switch_to.window(driver.window_handles[1])
        print('Entra com Govbr')
        botao_egov = {"xpath": '//*[@id="login-dados-certificado"]/p[2]/input'}
        aguarda(botao_egov)
        clica(botao_egov)
        sleep(5)
        botao_certificado = {"xpath": '//*[@id="cert-digital"]/button'}
        print('Certificado Digital')
        aguarda(botao_certificado)
        clica(botao_certificado)
        sleep(20)
    except WebDriverException:
        sleep(7)
        driver.execute_script("window.open('https://sso.acesso.gov.br/login?client_id=cav.receita.fazenda.gov.br', '_blank')")
        driver.switch_to.window(driver.window_handles[1])

def pegaTextoPagina():
    texto = 'Erro'
    try:
        iframe = driver.find_element(By.XPATH, '//*[@id="frameHtml"]')
        driver.switch_to.frame(iframe)
    except:
        iframe = driver.find_element(By.XPATH, '//*[@id="frameBinario"]')
        driver.switch_to.frame(iframe)
    numero = 1
    while texto == 'Erro' or texto == '':
        try:
            sleep(1)
            texto = driver.find_element(By.TAG_NAME, 'body').text
            numero = numero + 1
            if numero == 50:
                texto = 'Não localizou o texto'
        except:
            texto = 'não localizou texto'
    return texto
