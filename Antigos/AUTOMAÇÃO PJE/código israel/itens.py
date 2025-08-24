# Central de Pericia
agendar_e_administrar_perícia_médica_outras_especialidades = {'xpath': '//*[@title="Encaminhar para Agendar e administrar perícia médica - outras especialidades"]'}
encaminhar_para_Intimar_de_perícia = {'xpath': '//*[@title="Encaminhar para Intimar de perícia"]'}
# Central de Pericia
barra_opcoes_editor_tinymce = {'xpath': '//table[@id="grdBas"]'}
arquivo_permanente = {'xpath': '//*[@title="[JEF] Arquivo permanente"]'}
encaminhar_para_manter_processo_no_arquivo = {'xpath': '//*[@title="Encaminhar para Manter processo no arquivo"]'}

encaminhar_para_minutar_ato_ordinatorio = {'xpath': '//*[@title="Encaminhar para Minutar ato ordinatório"]'}
barra_lateral_esquerda = {'descricao': 'Barra que contém as opções "Assinaturas", "Tarefas", entre outras.',
                          'id': 'divSideBar'}
barra_rolagem_aba_tarefas = {'descricao': 'Aparece apos você clicar nao botão tarefas na barra lateral esquerda.',
                             'xpath': '//*[@id="divTarefasPendentes"//*@class="overflowTarefas"'}
body = {'descricao': 'Elemento body do HTML.', 'xpath': '//body'}
botao_abre_mais_detalhes = {'descricao': 'Abre a tela com o "mais detalhes" dos autos (na guia autos).',
                            'xpath': '//*[@id="navbar"]/ul/li/a[1]/span'}
adicionar_visualizacao_aba_lembrete = {'descricao': 'Botão adicionar da aba de lembrete',
                                       'xpath': '//div[@id="formLembretes:botoesPermissoes"]/input'}
visualizacoes_adicionadas = {'descricao': 'tbody contendo as visualizações dispoíveis para o lembrete que está sendo '
                                          'cadastrado', 'xpath': '//tr/td/h6'}
alert_lembrete_salvo = {'descricao': 'alerta que indica que o lembrete foi salvo',
                        'xpath': '//span[contains(text(), "Dados gravados com sucesso.")]'}
novo_lembrete = {'descricao': 'Botão novo lembrete localizado na janela de leitura de lembretes existente.',
                        'xpath': '//button[contains(text(), "Novo lembrete")]'}
janela_lembretes = {'descricao': 'Janela que mostra os lembretes existentes no processo.', 'id': 'modalLembretes'}
botao_etiqueta = {'descricao': 'Botão do canto superior direito que abre a lista de etiquetas.\n '
                               'utilizada para adicionar etiquetas', 'id': 'btn-gerenciar-etiquetas'}
botao_etiquetas_painel_usuario = {'descricao': 'Botão para o item etiquetas, localizado no painel de usuário ao'
                                               ' lado esquerdo da tela', 'id': 'tabEtiquetas_header'}
botao_logar_certificado = {'descricao': 'Botão da páginma inicial do PJe, responsável por logar pelo '
                                        'certificado digital', 'id': 'loginAplicacaoButton'}
botao_logar_certificado_cnj = {'descricao': 'Botão da páginma inicial do PJe, responsável por logar pelo '
                                        'certificado digital', 'id': 'kc-pje-office'}
botao_menu_esquerdo = {'descricao': 'Abre menu do lado esquerdo.', 'xpath': '//*[@class="botao-menu"]'}
botao_menu_guia_autos = {'descricao': 'Abre menu do lado direito da guia autos.', 'xpath': '//*[@title="Menu"]'}
botao_outras_opcoes = {'descricao': 'Necessário para movimentar os processos.', 'id': 'menu-mais-opcoes'}
botao_proxima_pagina = {'descricao': 'Botão que avança para a próxima página do páginador de processos.',
                        'xpath': '//*[@class ="ui-paginator-next ui-paginator-element ui-state-default ui-corner-all"]'}
botao_salvar_lembrete = {'descricao': 'Botão para salvar o lembrete.',
                         'xpath': '//div[@id="formLembretes:msgs"]/following-sibling::input[1]'}
botao_tarefas = {'descricao': 'Localizado ao lado direito do paginador de processos.\n'
                              'Utilizado para mostrar as caixas disponíveis.',
                 'xpath': '//*[@class= "fas fa-check-square fa-2x"]'}
botao_tela_inicial = {'descricao': 'Botão que volta para a tela inicial do painel do usuário.',
                      'xpath': '//*[@title="Tela inicial"]'}
aqui_sera_exibida_a_tarefa_selecionada = {'xpath': '//div[@class="nenhum-processo-selecionado ng-star-inserted"]'}
campo_com_quantidade_processos_na_caixa = {'descricao': 'Localizado ao lado do nome da caixa após clicar em uma caixa.',
                                           'xpath': '//*[@id="divActions"]/filtro-tarefas/div/div[1]/div[2]/span'}
campo_pesquisar_etiquetas = {'descricao': 'Campo disponível para digitar o nome da etiqueta que deseja incluir',
                             'xpath': '//*[@name="itPesquisarEtiquetas"]'}
campo_pesquisar_dentro_caixa = {'descricao': 'Campo localizado dentro da caixa, logo abaixo do nome dela',
                                'id': 'inputPesquisaTarefas'}
confirma_moveu = {'descricao': 'Aviso que aparece quando uma movimentação é realizada.',
                  'xpath': '//simple-notification/div/div[1]/div[1]'}
campo_para_digitar_lembrete = {'descricao': 'Campo para digitar o texto dos lembretes', 'id': 'formLembretes:descricao'}
encaminhar_para = {'descricao': 'Ícone localizado no canto superior direito da tela.', 'id': 'btnTransicoesTarefa'}
encaminhar_para_analise_secretaria = {'descricao': 'Opção utilizada para enviar o processo para a caixa'
                                                   ' "Análise secretaria"',
                                      'xpath': '//*[@title="Encaminhar para Análise de secretaria"]'}
encaminhar_para_controlar_pericia_propria_vara = {'descricao': 'Opção utilizada para enviar o processo para a caixa'
                                                               'controlar_pericia_propria_vara',
                                                  'xpath': '//*[@title='
                                                           '"Encaminhar para Controlar perícia na própria Vara"]'}
encaminhar_para_aguardar_juntada_laudo = {'descricao': 'Opção utilizada para enviar o processo para a caixa'
                                                               'aguardar juntada de laudo',
                                                  'xpath': '//*[contains(text(), "Aguardar juntada de laudo"]'}
encaminhar_lancar_movimento_de_pericia_designada_e_aguardar_juntada_de_laudo = {'descricao': '',
                                                  'xpath': '//*[@title="Encaminhar para Lançar movimento de perícia designada e aguardar juntada de laudo"]'}
encaminhar_para_agendar_e_administrar_audiencias = {'xpath': '//*[@title="Encaminhar para Agendar e administrar audiências cíveis"]'}
title="Encaminhar para Aguardar juntada de laudo"
encaminhar_para_aguardar_prazos_em_aberto = {'xpath': '//*[@title="Encaminhar para Aguardar prazos em aberto"]'}
encaminhar_para_aguardar_prazo_automatico = {'xpath': '//*[@title="Encaminhar para Aguardar prazo automático"]'}
encaminhar_para__criar_requisicao_pequeno_valor = {'xpath': '//a[@title="Encaminhar para Criar Requisição de Pequeno Valor"]'}
encaminhar_para_aguardando_migracao_rpv = {'xpath': '//*[@title="[JEF] Aguardando migração de RPV"]'}
encaminhar_para_arquivar = {'descricao': 'Opção arquivar utilizada para encaminhar um processo para o arquivo',
                            'xpath': '//*[@title="Encaminhar para Arquivar"]'}
encaminhar_para_arquivar_definitivamente = {'xpath': '//*[@title="Encaminhar para Arquivar definitivamente"]'}
encaminhar_para_assinatura = {'descricao': 'Opção utilizada para encaminhar um processo para assinatura',
                              'xpath': '//*[@title="Encaminhar para Encaminhar para assinatura"]'}
encaminhar_para_revisao = {'descricao': 'Opção utilizada para encaminhar um processo para revisão',
                              'xpath': '//*[@title="Encaminhar para Encaminhar para revisão"]'}
encaminhar_para_expedir_rpv = {'xpath': '//*[@title="Encaminhar para Expedir RPV - Precatório"]'}
encaminhar_para_nao_aguardar_prazo = {'xpath': '//*[@title="Encaminhar para Não aguardar prazo"]'}
encaminhar_para_juntar_certidao_automatica =  {'xpath': '//*[@title="Encaminhar para Juntar Certidão Automática (Administrador)"]'}
encaminhar_para_minutar_certidao = {'xpath': '//*[@title="Encaminhar para Minutar certidão"]'}
encaminhar_para_remeter_turma_recursal = {'descricao': 'Opção Remeter à Turma Recursal do encaminhar para',
                                          'xpath': '//*[@title="Encaminhar para Remeter à Turma Recursal"]'}
encaminhar_para_retornar_para_minuta = {'xpath': '//*[@title="Encaminhar para Retornar para minutar"]'}
encaminhar_para_cancelar_e_encaminhar_para_analise_de_secretaria = {'xpath': '//*[@title="Encaminhar para Cancelar e encaminhar para análise de secretaria"]'}
encaminhar_para_central_pericias = {'xpath': '//*[@title="Encaminhar para Central de Perícias"]'}
encaminhar_para_remeter_central_pericias = {'xpath': '//*[@title="Encaminhar para Remeter à Central de Perícias"]'}
encaminhar_para_conclusão_secretaria = {'xpath': '//*[@title="Encaminhar para Conclusão para julgamento - SEC"]'}
encaminhar_para_concluir_despacho_secretaria = {'xpath': '//*[@title="Encaminhar para Conclusão para despacho - SEC"]'}
encaminhar_para_preparar_comunicacao_e_outros_expedientes = \
    {'descricao': 'Opção Preparar comunicação e outros expedientes do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Preparar comunicação e outros expedientes"]'}
encaminhar_para_expedientes_assinados_pelo_sistema = \
    {'descricao': 'Opção Rotina em lote ou individual - expedientes PADRÃO assinado pelo sistema do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Rotina em lote ou individual - expedientes PADRÃO assinado pelo sistema - '
              'TODAS AS CEMANs DISPONÍVEIS"]'} 
encaminhar_para_intimacao_via_sistema_autores_5_dias = \
    {'descricao': 'Opção Intimação via Sistema autor(es) - 5 dias do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Intimação via Sistema autor(es) - 5 dias"]'}
encaminhar_para_intimacao_via_sistema_autores_10_dias = \
    {'descricao': 'Opção Intimação via Sistema autor(es) - 10 dias do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Intimação via Sistema autor(es) - 10 dias"]'}
encaminhar_para_intimacao_via_sistema_autores_15_dias = \
    {'descricao': 'Opção Intimação via Sistema autor(es) - 15 dias do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Intimação via Sistema autor(es) - 15 dias"]'}
encaminhar_para_intimacao_via_sistema_autores_30_dias = \
    {'descricao': 'Opção Intimação via Sistema autor(es) - 30 dias do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Intimação via Sistema autor(es) - 30 dias"]'}
encaminhar_para_intimacao_via_sistema_reus_5_dias = \
    {'descricao': 'Opção Intimação via Sistema reus - 5 dias do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Intimação via Sistema réu(s) - 5 dias"]'}
encaminhar_para_intimacao_via_sistema_reus_10_dias = \
    {'descricao': 'Opção Intimação via Sistema reus - 10 dias do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Intimação via Sistema réu(s) - 10 dias"]'}
encaminhar_para_intimacao_via_sistema_reus_15_dias = \
    {'descricao': 'Opção Intimação via Sistema reus - 15 dias do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Intimação via Sistema réu(s) - 15 dias"]'}
encaminhar_para_intimacao_via_sistema_reus_30_dias = \
    {'descricao': 'Opção Intimação via Sistema reus - 30 dias do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Intimação via Sistema réu(s) - 30 dias"]'}
encaminhar_para_intimacao_via_sistema_todos_5_dias = \
    {'descricao': 'Opção Intimação via Sistema todos - 5 dias do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Intimação via Sistema todos - 5 dias"]'}
encaminhar_para_intimacao_via_sistema_todos_10_dias = \
    {'descricao': 'Opção Intimação via Sistema todos - 10 dias do encaminhar para',
     'xpath': '//*[@title="Encaminhar para Intimação via Sistema todos - 10 dias"]'}
encaminhar_para_rotina_individual = {'xpath': '//*[@title="Encaminhar para Rotina individual - TODAS AS CEMANs DISPONÍVEIS"]'}
encaminhar_para_ignorar_pendencia_apreciacao_gratuidade = {'xpath': '//*[@title="Encaminhar para Ignorar pendência de apreciação de gratuidade"]'}
encaminhar_para_cancelar_e_avancar = {'xpath': '//*[@title="Encaminhar para Cancelar e avançar"]'}
encaminhar_para_retornar_para_aguardar_migracao_de_rpv = {'xpath': '//*[@title="Encaminhar para Retornar para aguardar migração de RPV"]'}
encaminhar_para_retornar = {'xpath': '//*[@title="Encaminhar para Retornar"]'}
encaminhar_para_Juntar_resposta = {'xpath': '//*[@title="Encaminhar para Juntar resposta"]'}
encaminhar_para_Juntar_prosseguir = {'xpath': '//*[@title="Encaminhar para Prosseguir"]'}
retornar_para_preparar_rpv = {'xpath': '//*[@title="Encaminhar para Retornar para preparar RPV"]'}
retornar_para_escolher_tipo_de_requisicao_de_pagamento = {'xpath': '//*[@title="Encaminhar para Retornar para escolher tipo de requisição de pagamento"]'}
retornar_para_cancelar = {'xpath': '//*[@title="Encaminhar para Cancelar"]'}
prosseguir = {'xpath': '//*[@title="Encaminhar para Prosseguir"]'}
expedientes = {'descricao': 'Opção do menu da guia autos que ao ser clicado abre a guia expediente.',
               'id': 'navbar:linkAbaExpedientes'}
frame_login = {'id': 'ssoFrame'}
frame_editor = {'descricao': 'Necessário trocar para este frame antes de inicializar a manipulação dos documentos.'}
frame_painel_usuario = {'descricao': "Frame do CNJ."}
frame_trf1 = {'descricao': "Frame do TRF1, faz movimentações atos, entre outros. Arrumar isso."}
frame_lotacao = {'descricao': "Frame para escolher lotação e botão abrir menu (de fato é o HTML)."}
lista_lotacao = {'descricao': 'Lista com todas as lotações disponíeis para o usuário.'
                              '\nPara utilizar é necessário clicar no nome do usuário primeiro.',
                 'id': 'papeisUsuarioForm:usuarioLocalizacaoDecoration:usuarioLocalizacao'}
lista_processos = {'descricao': 'Esta é a lista com todos os processos que aparecem na página atual do paginador',
                   'xpath': '//*[@class="ui-datalist-data"]'}
mais_detalhes = {'descricao': 'Este elemento possui o o texto dos detalhes dos processos. Ex.: Tutela'
                              '\nAtualmente utilizado para confirmar se a guia autos está aberta.'
                              '\nPara acessar os valores (SIM ou NÃO), utilize "valores_mais_detalhes" ',
                 '': 'maisDetalhes', 'xpath': '//*[@id="maisDetalhes"]'}
nome_do_usuario = {'descricao': 'Dopbox localizado no campo que contém o nome do usuário.',
                   'xpath': '//*[@class="hidden-xs nome-sobrenome tip-bottom"]'}
numeros_processos_analisados = []
numeros_processos_movimentados = []
opcao_autos = {'descricao': 'Opção do menu hamburguer do lado direito que retorna para a guia autos.',
               'id': 'navbar:linkAbaAutos'}
opcao_painel = {'descricao': 'Opção painel do menu localizado ao lado esquerdo da tela.',
                'linktext': 'Painel'}
opcao_painel_usuario = {'descricao': 'Opção painel do usuário do menu localizado ao lado esquerdo da tela.',
                        'linktext': 'Painel do usuário'}
documento_caixa_avaliar_ato = {'descricao': 'Representa o documento que foi assinado. Este documento aparece na mesma'
                                            'guia que o paginador e não na guia autos.',
                               'id': 'paginaInteira'}
pagina_atual_paginador = {'descricao': 'Este item representa a pagina atual do paginador.'
                                       '\nSempre existe mesmo que só haja uma página',
                          'xpath': '//*[@class= "pui-paginator-page pui-paginator-element '
                                   'ui-state-default ui-corner-all ng-binding ng-scope ui-state-active"]'}
paginador = {'xpath': '//*[@id="divProcessosTarefa"]/div[2]'}
carregando = {'descricao': 'Este item representa a  círculo que aparece quando você troca de página',
              'xpath': '//*[@class="loaderWrapper ng-star-inserted"]'}
painel_tarefas = {'descricao': 'Painel de tarefas que contím todas as caixas disponíveis.',
                  'id': "tabTarefas_content"}
quadro_de_avisos = {'descricao': 'Quadro de avisos que aparece quando você escolhe lotação',
                    'id': 'avisosPannel_header'}

tabela_expedientes = {'descricao': 'Tabela contendo os dados de todos os expedientes',
                      'id': 'processoParteExpedienteMenuGridList'}

timeline = {'descricao': 'Timeline da aba autos.', 'id': 'divTimeLine:divEventosTimeLine'}
select_jurisdicao_remeter_tr = {'descricao': 'Select de remeter tr', 'xpath': '//div[contains(@id,"formularioDadosIniciais")]//select[contains(@id,"jurisdicaoCombo")]'}
select_classe_judicial_remeter_tr = {'descricao': 'Select de remeter tr', 'xpath': '//div[contains(@id,"formularioDadosIniciais")]//select[contains(@id,"comboClasseJudicial")]'}
select_motivo_remessa_remeter_tr = {'descricao': 'Select de remeter tr', 'xpath': '//div[contains(@id,"formularioDadosIniciais")]//select[contains(@id,"comboClasseMotivoRemessa")]'}

campo_com_assunto_principal_da_tarefa_remeter_tr = { 'xpath': '//div[contains(@id,"edtAssuntosResumoProcesso2:sd")]'}
aba_dados_iniciais_da_tarefa_remeter_tr = {'xpath': '//td[contains(@id,"form_lbl")]'}
aba_processo_da_tarefa_remeter_tr = {'xpath': '//td[contains(@id,"informativo_lbl")]'}
aba_partes_da_tarefa_remeter_tr = {'xpath': '//td[contains(@id,"tabPartes_lbl")]'}
botao_inverter_polo_aba_partes_da_tarefa_remeter_tr = {'xpath': '//input[contains(@id,"inverterPolo")]'}
botao_gravar_aba_processo_da_tarefa_remeter_tr = {'xpath': '//input[contains(@id,"confirmar")]'}
botao_remeter_aba_processo_da_tarefa_remeter_tr = {'xpath': '//input[contains(@id,"remeter")]'}
mensagem_configuracao_remessa_gravada = {'xpath': '//*[contains(text(), "Configuração da remessa gravada!")]'}

tag_a_com_processo_e_caixa_autal = {'xpath': '//*[@id="frameTarefas"]/div/div[1]/div[1]/div/div[1]/a'}

lista_etiquetas_para_vincular = {'xpath': '//table[@class="table table-hover table-striped table-etiquetas"]'}

campo_numeros_processos_separados_por_virgula_duplica_processos = {
    'descricao': 'Campo onde inserimos os números dos processos que serão duplicados',
    'xpath': '//div[@id="fPP:consultaSearchForm"]/div/div/div[2]/input'
}
