import os
from PyQt6.QtWidgets import QMessageBox
from model.conexao_cliente import ClienteRede
from .trabalhadora import Worker

class ControladorCliente:
    def __init__(self, janela):
        self.janela = janela
        
        host = os.environ.get('SERVER_HOST', 'localhost')
        porta = int(os.environ.get('SERVER_PORT', 5000))
        self.modelo = ClienteRede(host=host, porta=porta)
        
        self.janela.pagina_login.solicitar_login.connect(self.processar_login)
        self.janela.pagina_registro.dados_registro.connect(self.processar_registro)
        
        self.worker = None
        
        # variaveis da sessao
        self.id_usuario = None
        self.id_quadro = None
        self.id_quadro_sala = None

    def processar_login(self, usuario, senha, sala=None):
        if not usuario or not senha:
            QMessageBox.warning(self.janela, "Erro", "Por favor, preencha todos os campos")
            return
            
        #payload = {"username": usuario, "password": senha, "sala": sala}
        # Mudei aqui, gustavo. 
        payload = {"nomeUsuario": usuario, "senhaUsuario": senha, "sala": sala}
        self.iniciar_requisicao_background('LOGIN', payload)

    def processar_registro(self, usuario, senha):
        if not usuario or not senha:
            QMessageBox.warning(self.janela, "Erro", "Por favor, preencha todos os campos")
            return
            
        #payload = {"username": usuario, "password": senha}
        # mudei aqui, gustavo.
        payload = {"nomeUsuario": usuario, "senhaUsuario": senha}
        self.iniciar_requisicao_background('REGISTER', payload)

    def iniciar_requisicao_background(self, tipo, payload):
        self.janela.definir_carregamento(True)
        
        self.worker = Worker(self.modelo, tipo, payload)
        self.worker.sinal_resultado.connect(self.ao_receber_resposta)
        self.worker.sinal_erro.connect(self.ao_ocorrer_erro)
        
        self.worker.start()
        print(f"Enviando {tipo} para o servidor")

    def ao_receber_resposta(self, resposta):
        self.janela.definir_carregamento(False)
        if resposta['sucesso']:
            dados = resposta.get('dados', {})
            
            # Sucesso no login
            if 'idUsuario' in dados:
                self.id_usuario = dados.get('idUsuario')
                sala_digitada = dados.get('sala') 
                
                # se tiver sala tenta entrar
                if sala_digitada:
                    payload = {"idUsuario": self.id_usuario, "idQuadroSala": sala_digitada}
                    self.iniciar_requisicao_background('JOIN_QUADRO', payload)
                else:
                    payload = {"idUsuarioDono": self.id_usuario}
                    self.iniciar_requisicao_background('CREATE_QUADRO', payload)
            
            # sucesso no entrar quadro
            elif 'idQuadro' in dados:
                self.id_quadro = dados.get('idQuadro')
                self.id_quadro_sala = dados.get('idQuadroSala')
                
                QMessageBox.information(
                    self.janela, 
                    "Conectado ao Quadro", 
                    f"Entrou na sala: {self.id_quadro_sala}"
                )
                
                self.janela.pagina_principal.definir_sala(self.id_quadro_sala)
                self.janela.mudar_pagina(2)
                
            else:
                QMessageBox.information(self.janela, "Sucesso", resposta['mensagem'])
                if self.janela.obter_indice_atual() == 1:
                    self.janela.mudar_pagina(0)
        else:
            QMessageBox.critical(self.janela, "Erro", resposta['mensagem'])

    def ao_ocorrer_erro(self, mensagem_erro):
        self.janela.definir_carregamento(False)
        QMessageBox.critical(self.janela, "Erro de Sistema", f"Ocorreu um erro inesperado: {mensagem_erro}")
