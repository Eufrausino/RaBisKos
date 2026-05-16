import os
from PyQt6.QtWidgets import QMessageBox
from model.cliente_rede import ClienteRede
from .worker import Worker

class ControladorCliente:
    def __init__(self, janela):
        self.janela = janela
        
        host = os.environ.get('SERVER_HOST', 'localhost')
        porta = int(os.environ.get('SERVER_PORT', 5000))
        self.modelo = ClienteRede(host=host, porta=porta)
        
        self.janela.pagina_login.requisitar_login.connect(self.processar_login)
        self.janela.pagina_registro.requisitar_registro.connect(self.processar_registro)
        
        self.worker = None

    def processar_login(self, usuario, senha):
        if not usuario or not senha:
            QMessageBox.warning(self.janela, "Erro", "Por favor, preencha todos os campos")
            return
            
        payload = {"username": usuario, "password": senha}
        self.iniciar_requisicao_background('LOGIN', payload)

    def processar_registro(self, usuario, senha):
        if not usuario or not senha:
            QMessageBox.warning(self.janela, "Erro", "Por favor, preencha todos os campos")
            return
            
        payload = {"username": usuario, "password": senha}
        self.iniciar_requisicao_background('REGISTER', payload)

    def iniciar_requisicao_background(self, tipo, payload):
        # Desabilita interface durante o carregamento
        self.janela.definir_carregamento(True)
        
        # Cria e configura o Worker
        self.worker = Worker(self.modelo, tipo, payload)
        self.worker.sinal_resultado.connect(self.ao_receber_resposta)
        self.worker.sinal_erro.connect(self.ao_ocorrer_erro)
        
        # Inicia thread
        self.worker.start()

    def ao_receber_resposta(self, resposta):
        self.janela.definir_carregamento(False)
        if resposta['sucesso']:
            QMessageBox.information(self.janela, "Sucesso", resposta['mensagem'])
            
            # Se o login foi bem sucedido (estava na página 0), vai para a Home (página 2)
            if self.janela.obter_indice_atual() == 0:
                self.janela.mudar_pagina(2)
            # Se o registro foi bem sucedido (estava na página 1), volta para o Login (página 0)
            elif self.janela.obter_indice_atual() == 1:
                self.janela.mudar_pagina(0)
        else:
            QMessageBox.critical(self.janela, "Erro", resposta['mensagem'])

    def ao_ocorrer_erro(self, mensagem_erro):
        self.janela.definir_carregamento(False)
        QMessageBox.critical(self.janela, "Erro de Sistema", f"Ocorreu um erro inesperado: {mensagem_erro}")
