from bs4 import BeautifulSoup
import re
import web


def retira_o_que_nao_eh_processo(lis):
    lis.remove(lis[0])
    lis.remove(lis[0])
    return lis


def encontra_juiz(j):
    try:
        span = j.find_all('span')[10]
        texto = span.text
        juiz = texto[texto.index('Juiz Federal'): -1]
        return juiz
    except ValueError as erro_original:
        raise ValueError('Quantidade de spans incorreta, o card foi modificado.')


def encontra_orgao_julgador(j):
    try:
        span = j.find_all('span')[10]
        texto = span.text
        orgao_julgador = texto[texto.index('Juiz Federal'): -1]
        return orgao_julgador
    except ValueError as erro_original:
        raise ValueError('Quantidade de spans incorreta, o card foi modificado.')


def encontra_assunto(j):
    assunto = j.find_all('span')[9].text
    return assunto


def encontra_partes(j):
    spans = j.find_all('span')
    for span in spans:
        try:
            texto = span.text
            divisor = texto.index(' X ')
            parte_autora = texto[0: divisor]
            reu = texto[divisor + 3:]
            return parte_autora, reu
        except ValueError:
            continue


def encontra_ultima_movimentacao(j):
    try:
        ultima_movimentacao = j.find_all('span')[16].text
    except IndexError:
        ultima_movimentacao = 'Última movimentação não localizada'
    return ultima_movimentacao


def encontra_etiquetas(j):
    spans = j.find_all('span')
    lista_etiquetas = []
    marcador = 17
    if len(spans) > 15:
        while marcador < len(spans):
            lista_etiquetas.append(spans[marcador].text)
            marcador += 2
    return lista_etiquetas


def encontra_data_entrada_caixa(j):
    return j.find('processo-datalist-card').div.div.find_all('div')[1].span.text


def encontra_lotacao(j):
    data_card = j.find('processo-datalist-card')
    spans = data_card.div.find_all('span')
    for span in spans:
        try:
            lotacao = span.text.split('/')[1].strip()
        except IndexError:
            continue
    return lotacao


def cria_lista_processos(tag_paginador, processos_a_serem_gerados):
    from processo import ProcessoSimples
    soup = BeautifulSoup(tag_paginador, 'html.parser')
    lis = soup.find_all('li')
    lis = retira_o_que_nao_eh_processo(lis)
    resultado = []        
    for i in processos_a_serem_gerados.copy():
        for j in lis:
            if i in j.text:
                dados_processo = dict()
                dados_processo['data_entrada_na_caixa'] = encontra_data_entrada_caixa(j)
                dados_processo['lotacao'] = encontra_lotacao(j)
                dados_processo['numero'] = i
                dados_processo['assunto'] = encontra_assunto(j)
                dados_processo['juiz'] = encontra_juiz(j)
                dados_processo['orgao_julgador'] = encontra_orgao_julgador(j)
                dados_processo['parte_autora'], dados_processo['reu'] = encontra_partes(j)
                dados_processo['ultima_movimentacao'] = encontra_ultima_movimentacao(j)
                dados_processo['etiquetas'] = encontra_etiquetas(j)
                processo = ProcessoSimples(dados_processo)
                resultado.append(processo)
    return resultado


def busca_divs_de_documentos_timeline(div_movimentacoes):
    lista_div = []
    div_movimentacoes = div_movimentacoes.div
    # Retira a tag data de rolagem se não tiver retira há documento não lido
    try:
        div_movimentacoes.find_all("div", {'class': 'media data div-data-rolagem'})[0].decompose()
    except IndexError:
        div_movimentacoes.find_all("div", {'class': 'btn-group btn-group-sm mt-5'})[0].decompose()
    for child in div_movimentacoes.children:
        if child != '\n':
            lista_div.append(child)
    return lista_div


def veh_se_eh_data(i):
    classe = i.get_attribute_list('class')
    return True if 'data' in classe else False


def encontra_parte_que_juntou(div):
    span = div.find('span')
    resultado = span.get('data-original-title')
    if resultado is None:
        resultado = span.get('title')
    return resultado.lower()


def encontra_movimentos(divs):
    lista_spans = divs.find_all('span', class_='text-upper texto-movimento')
    lista_movimentacoes = []
    for i in lista_spans:
        lista_movimentacoes.append(i.text.lower())
    return lista_movimentacoes


def encontra_id_titulo_e_link(documento):
    string = documento.find('span')
    if string == None:
        return 'documento excluído', 'documento excluído', 'documento excluído'
    texto_string = string.text.lower()
    try:
        indice = texto_string.index(' - ')
    except ValueError as err:
        return 'Erro documento não existente', 'Erro documento não existente', 'Erro documento não existente'
    id_doc = texto_string[0:indice]
    titulo_doc = texto_string[indice+3:]
    id_link = documento.get('id')
    link_doc = {'ID':id_link}
    return id_doc, titulo_doc, link_doc


def encontra_documento(div_midia_body):
    div_documento = div_midia_body.find('a')
    id_doc, titulo_doc, link_doc = encontra_id_titulo_e_link(div_documento)
    documento = {'id': id_doc, 'titulo': titulo_doc, 'link': link_doc}
    return documento


def encontra_anexos(div_anexos_da_div_midia_body):
    lista_anexos = []
    ul = div_anexos_da_div_midia_body.find('ul')
    if ul is None:
        return []
    lis = ul.find_all('li')
    for i in lis:
        tag_anexo = i.find('a')
        id_doc, titulo_doc, link_doc = encontra_id_titulo_e_link(tag_anexo)
        anexo = {'id':id_doc, 'titulo':titulo_doc, 'link':link_doc}
        lista_anexos.append(anexo)
    return lista_anexos


def encontra_documento_e_anexos(divs):
    div_anexos_da_div_midia_body = divs.find('div', class_='anexos')
    documento = encontra_documento(div_anexos_da_div_midia_body)
    documento['anexos'] = encontra_anexos(div_anexos_da_div_midia_body)
    return documento


def tem_documento(tag):
    resultado = tag.find('a')
    return False if resultado == None else True


def veh_se_eh_preloader(div):
    classe = div.get_attribute_list('class')
    return True if 'media' not in classe else False


def gera_documentos_da_data(data, lista_divs_documentos, i):
    lista_documentos = []
    marcador = 1
    for j in lista_divs_documentos:
        posicao_proximo_documento = lista_divs_documentos.index(i) + marcador
        try:
            div_proximo_documento = lista_divs_documentos[posicao_proximo_documento]
        except IndexError:
            break
        if veh_se_eh_data(div_proximo_documento):
            break
        if veh_se_eh_preloader(div_proximo_documento):
            break
        else:
            divs = div_proximo_documento.find_all('div')
            quem_juntou = encontra_parte_que_juntou(divs[0])
            lista_movimentacao = encontra_movimentos(divs[1])
            if tem_documento(divs[1]):
                documento = encontra_documento_e_anexos(divs[1])
            else:
                documento = {}
            documento['data'] = data
            documento['quem_juntou'] = quem_juntou
            documento['lista_movimentacoes'] = lista_movimentacao
            lista_documentos.append(documento)
            marcador += 1
    return lista_documentos


def gera_lista_timeline(lista_divs_documentos):
    timeline = []

    for i in lista_divs_documentos:
        if veh_se_eh_data(i):
            data = i.find('span').text
            lista_documentos_da_data = gera_documentos_da_data(data, lista_divs_documentos, i)
            for i in lista_documentos_da_data:
                posicao = lista_documentos_da_data.index(i)
                timeline.append(lista_documentos_da_data[posicao])
        else:
            continue
    return timeline


def encontra_timeline(soup):
    timeline = soup.find(id='divTimeLine')
    div_movimentacoes = timeline.find(id='divTimeLine:divEventosTimeLine')
    lista_divs_documentos = busca_divs_de_documentos_timeline(div_movimentacoes)
    timeline = gera_lista_timeline(lista_divs_documentos)
    return timeline


def encontra_dados_autos(tag_body):
    soup = BeautifulSoup(tag_body, 'html.parser')
    mais_detalhes = soup.find(id='maisDetalhes')
    dados_autos_completos = dict()
    dds = mais_detalhes.find_all('dd')
    if re.findall("[0-9]{7}-[0-9]{2}\.[0-9]{4}\.[0-9]\.[0-9]{2}\.[0-9]{4}", dds[2].text):
        dds.remove(dds[2])
    dados_autos_completos['Classe judicial'] = dds[0].text
    lis = dds[1].find_all('li')
    assunto_js = web.driver.execute_script(
        'return document.querySelector("#maisDetalhes > dl > dd:nth-child(4)").textContent')
    result = assunto_js.split('/')
    # Remove leading and trailing whitespaces from each element
    result = [item.strip() for item in result]
    #dados_autos_completos['Assunto'] = [x.text for x in lis]
    dados_autos_completos['Assunto'] = result
    dados_autos_completos['Jurisdição'] = dds[2].text
    dados_autos_completos['Autuação'] = dds[3].text
    dados_autos_completos['Última distribuição'] = dds[4].text
    dados_autos_completos['Valor da causa'] = dds[5].text
    dados_autos_completos['Segredo de justiça?'] = dds[6].text
    dados_autos_completos['Justiça gratuita?'] = dds[7].text
    dados_autos_completos['Tutela/liminar?'] = dds[8].text
    dados_autos_completos['Prioridade?'] = dds[9].text
    dados_autos_completos['Competência'] = dds[12].text
    dados_autos_completos['timeline'] = encontra_timeline(soup)
    try:
        lis = soup.find("div", {"id": "poloAtivo"}).table.tbody.tr.td.ul.find_all('li')
        dados_autos_completos['advogado_parte_autora'] = [x.span.text[:-34] for x in lis if '(ADVOGADO)' in x.span.text]
    except AttributeError:
        dados_autos_completos['advogado_parte_autora'] = 'atermação'

    return dados_autos_completos


def tira_expedientes_da_tabela(html):
    soup = BeautifulSoup(html, 'html.parser')
    tbody = soup.tbody
    lista_tr = tbody.find_all('tr')
    lista_expedientes = []
    for i in lista_tr:
        if 'Verificar Entrega' in i.text:
            break
        expediente = {}
        lista_td = i.find_all('td')
        expediente['Ato de comunicação'] = lista_td[0].text
        expediente['fechado'] = lista_td[3].text
        lista_expedientes.append(expediente)
    return lista_expedientes


def devolve_lembretes(html):
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find_all('div', class_="panel-body")
    recados = [recado.text.strip() for recado in result]
    for i in recados:
        if i == 'Intimação por whatsapp':
            recados[recados.index(i)] = 'Intimação por whatsapp;'
    return recados

def encontra_numeros_processos(html):
    soup = BeautifulSoup(html, 'html.parser')
    resultado = []
    for processo in soup.find_all("processo-datalist-card"):
        resultado.append(processo.div.div.next_sibling.next_sibling.a.div.span.next_sibling.text.strip()[-25:])
    return resultado
