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
        self.janela.pagina_principal.elemento_criado.connect(self.processar_criacao_elemento)

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
            
            # 1. SUCESSO NO LOGIN
            if 'idUsuario' in dados:
                self.id_usuario = dados.get('idUsuario')
                sala_digitada = dados.get('sala') 
                
                if sala_digitada:
                    payload = {"idUsuario": self.id_usuario, "idQuadroSala": sala_digitada}
                    self.iniciar_requisicao_background('JOIN_QUADRO', payload)
                else:
                    payload = {"idUsuarioDono": self.id_usuario}
                    self.iniciar_requisicao_background('CREATE_QUADRO', payload)
                    
            # 2. SUCESSO AO ENTRAR/CRIAR QUADRO
            elif 'idQuadroSala' in dados:
                self.id_quadro = dados.get('idQuadro')
                self.id_quadro_sala = dados.get('idQuadroSala')
                
                QMessageBox.information(
                    self.janela, 
                    "Conectado ao Quadro", 
                    f"Entrou na sala: {self.id_quadro_sala}"
                )
                
                self.janela.pagina_principal.definir_sala(self.id_quadro_sala)
                self.janela.mudar_pagina(2)
                
                # Liga o "ouvido" do multiplayer
                self.iniciar_escuta_tempo_real()
                
                # CORREÇÃO AQUI: Em vez de iniciar um Worker, enviamos direto sem esperar (a Thread de escuta vai apanhar a resposta)
                self.modelo.enviar_requisicao('GET_QUADRO', {"idQuadro": self.id_quadro}, esperar_resposta=False)
                
            else:
                QMessageBox.information(self.janela, "Sucesso", resposta['mensagem'])
                if self.janela.obter_indice_atual() == 1:
                    self.janela.mudar_pagina(0)
        else:
            QMessageBox.critical(self.janela, "Erro", resposta['mensagem'])
    
    def ao_ocorrer_erro(self, mensagem_erro):
        self.janela.definir_carregamento(False)
        QMessageBox.critical(self.janela, "Erro de Sistema", f"Ocorreu um erro inesperado: {mensagem_erro}")

    def processar_criacao_elemento(self, dados_elemento):
        # Só envia para o banco se estiver dentro de uma sala
        if not self.id_quadro:
            return 
            
        dados_elemento["idQuadro"] = self.id_quadro
        
        # Envia a requisição JSON para o Servidor TCP!
        self.iniciar_requisicao_background('CREATE_ELEMENTO', dados_elemento)

    def iniciar_escuta_tempo_real(self):
        from .trabalhadora import ThreadEscuta
        self.thread_escuta = ThreadEscuta(self.modelo)
        self.thread_escuta.sinal_evento.connect(self.processar_evento_rede)
        self.thread_escuta.start()

    def processar_evento_rede(self, evento):
        tipo = evento.get("type")
        dados = evento.get("data", {})

        if tipo == "ELEMENT_CREATED":
            self.janela.pagina_principal.adicionar_elemento_rede(dados)

        elif tipo == "GET_BOARD_RESPONSE":
            if 'elementos' in dados:
                for el in dados['elementos']:
                    self.janela.pagina_principal.adicionar_elemento_rede(el)

    def processar_criacao_elemento(self, dados_elemento):
        if not self.id_quadro:
            return 
        dados_elemento["idQuadro"] = self.id_quadro
        self.modelo.enviar_requisicao('CREATE_ELEMENTO', dados_elemento, esperar_resposta=False)