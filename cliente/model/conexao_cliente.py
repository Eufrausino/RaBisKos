import socket
# import json
# import struct
import os
import logging
import Pyro5.api
import queue
import threading

@Pyro5.api.expose
class ClienteRede:
    def __init__(self, host=None, porta=None):
        # self.host = host
        # self.porta = porta
        if "NS_HOST" in os.environ:
            self.host = os.environ.get("NS_HOST")
            self.porta = int(os.environ.get("NS_PORT", 9090))
        else:
            self.host = host or "localhost"
            self.porta = porta or 9090
        
        # Define a configuração global do Pyro5 para que os proxies resolvam PYRONAME corretamente
        from Pyro5 import config
        config.NS_HOST = self.host
        config.NS_PORT = self.porta

        self.servidor_proxy = None
        self.async_servidor_proxy = None
        self.daemon = None

        self.fila_eventos = queue.Queue()
        
        self.conectar()

    def conectar(self):
        try:
            logging.debug(f"[PYRO] Localizando Name Server em {self.host}:{self.porta}...")
            ns = Pyro5.api.locate_ns(host=self.host, port=self.porta)
            
            self.servidor_proxy = Pyro5.api.Proxy("PYRONAME:rabiskos.servidor")
            
            self.async_servidor_proxy = Pyro5.api.Proxy("PYRONAME:rabiskos.servidor")

            # CLIENT_HOST deve ser o IP desta máquina acessível pelo servidor (ex: 192.168.0.X)
            # Se não definido, tenta resolver automaticamente (pode falhar em Windows com 127.0.0.1)
            client_host = os.environ.get("CLIENT_HOST", socket.gethostbyname(socket.gethostname()))
            self.daemon = Pyro5.api.Daemon(client_host)
            self.daemon.register(self) # Registra o próprio cliente como alvo do callback

            threading.Thread(target=self.daemon.requestLoop, daemon=True).start()
            logging.info("[PYRO] Conexão com o middleware estabelecida com sucesso.")
            
        except Exception as e:
            logging.error(f"[ERRO REDE] Falha ao conectar ao sistema distribuído: {e}")
            raise e

    # def conectar(self):
    #     try:
    #         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         self.socket.connect((self.host, self.porta))
    #         return True
    #     except Exception as e:
    #         logging.debug(f"Erro de conexão: {e}")
    #         return False

    def enviar_requisicao(self, tipo_requisicao, payload, esperar_resposta=True):
        mensagem = {"type": tipo_requisicao, "data": payload}

        if esperar_resposta:
            try:
                self.servidor_proxy._pyroClaimOwnership()
                resposta_servidor = self.servidor_proxy.handle_message(mensagem, client_callback=self)
                
                # Adapta o formato da ResponseView do servidor para o formato que a sua Controller espera
                sucesso = resposta_servidor.get("status") == "ok"
                return {
                    "sucesso": sucesso,
                    "dados": resposta_servidor.get("data", {}),
                    "mensagem": resposta_servidor.get("message", tipo_requisicao if sucesso else resposta_servidor.get("code"))
                }
            except Exception as e:
                logging.error(f"Erro na requisição síncrona {tipo_requisicao}: {e}")
                return {"sucesso": False, "dados": {}, "mensagem": str(e)}
        else:
            # Se não precisa esperar resposta, usa o proxy assíncrono.
            # Isso impede que chamadas feitas na UI Thread (como desenhar) causem micro-travamentos.
            self.async_servidor_proxy.handle_message(mensagem, client_callback=self)
            return {}
        # if not self.socket:
        #     if not self.conectar():
        #         return {"sucesso": False, "mensagem": "Não foi possível conectar ao servidor"}
        
        # try:
        #     requisicao = {
        #         "type": tipo_requisicao,
        #         #mudei aqui gustavo, antes era "payload" no lugar de "data"
        #         "data": payload
        #     }
        #     # dados = json.dumps(requisicao).encode('utf-8')
        #     # cabecalho = struct.pack('>I', len(dados))
        #     # self.socket.sendall(cabecalho + dados)
        #
        #     if not esperar_resposta:
        #         return {"sucesso": True, "mensagem": "Enviado"}
        #
        #     # Ler resposta
        #     cabecalho = self.socket.recv(4)
        #     if not cabecalho:
        #         return {"sucesso": False, "mensagem": "Servidor fechou a conexão"}
        #
        #     tamanho_mensagem = struct.unpack('>I', cabecalho)[0]
        #     dados = b''
        #     while len(dados) < tamanho_mensagem:
        #         chunk = self.socket.recv(tamanho_mensagem - len(dados))
        #         if not chunk:
        #             break
        #         dados += chunk
        #
        #     resposta = json.loads(dados.decode('utf-8'))
        #     # mudei aqui gustavo. acrescentei as 5 linhas de baixo antes de return. 
        #     sucesso = resposta.get('status') == 'ok'
        #     if sucesso:
        #         mensagem = resposta.get('data', {}).get('mensagem', '')
        #     else:
        #         mensagem = resposta.get('message', '')
        #     return {
        #         # "sucesso": resposta.get('success', False),
        #         # "mensagem": resposta.get('message', '')
        #
        #         # mudei aqui gustavo.
        #         "sucesso": sucesso,
        #         "mensagem": mensagem,
        #         "dados": resposta.get('data', {})
        #     }
        # except Exception as e:
        #     self.socket = None 
        #     return {"sucesso": False, "mensagem": f"Erro de rede: {e}"}

    # def fechar(self):
    #     if self.socket:
    #         self.socket.close()
    #         self.socket = None
    #
    # def escutar_servidor(self):
    #     try:
    #         cabecalho = self.socket.recv(4)
    #         if not cabecalho:
    #             return None
    #
    #         tamanho_mensagem = struct.unpack('>I', cabecalho)[0]
    #         dados = b''
    #         while len(dados) < tamanho_mensagem:
    #             chunk = self.socket.recv(tamanho_mensagem - len(dados))
    #             if not chunk:
    #                 return None
    #             dados += chunk
    #
    #         return json.loads(dados.decode('utf-8'))
    #     except Exception:
    #         return None

    @Pyro5.api.oneway
    def notificar_evento(self, message: dict) -> None:
        """
        MÉTODO OBRIGATÓRIO PARA O PYRO5.
        Invocado remotamente pelo ConnectionManager do Servidor durante os Broadcasts.
        """
        logging.debug(f"[CALLBACK PYRO] Evento recebido do servidor: {message.get('type')}")
        self.fila_eventos.put(message)

    def escutar_servidor(self) -> dict:
        try:
            return self.fila_eventos.get(block=True)
        except Exception:
            return {}
