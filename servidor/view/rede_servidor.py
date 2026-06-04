# import threading
import logging
from model.banco_de_dados.banco import inicializar_banco
# from controller.client_handler import ClientHandler
from controller.server_controller import ServerController
import os
import Pyro5.api

class ServidorRede:
    """
    Camada de Visão (Interface) do Servidor.
    Responsável por gerenciar conexões TCP, threads e o protocolo de comunicação.
    """
    
    def __init__(self, host='0.0.0.0', porta=5000):
        if "SERVIDOR_HOST" in os.environ:
            self.host = os.environ.get("SERVIDOR_HOST")
        else:
            self.host = host
        self.porta = porta
        self.daemon = None
        self.server_controller = ServerController()

    def iniciar(self):
        inicializar_banco()
        
        # self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.servidor.bind((self.host, self.porta))
        # self.servidor.listen()
        
        logging.debug(f"[ESCUTANDO] Servidor MVC rodando em {self.host}:{self.porta}")
       
        try:
            self.daemon = Pyro5.api.Daemon(host=self.host, port=self.porta)
            
            uri = self.daemon.register(self.server_controller)
            logging.debug(f"[PYRO] Controller registrada no Daemon local. URI: {uri}")
            
            ns_host = os.environ.get("NS_HOST", "nameserver")
            ns_port = int(os.environ.get("NS_PORT", 9090))
            
            logging.info(f"[MIDDLWARE] Buscando Name Server em {ns_host}:{ns_port}...")
            ns = Pyro5.api.locate_ns(host=ns_host, port=ns_port)
            ns.register("rabiskos.servidor", uri)

            logging.info("[STATUS] Serviço 'rabiskos.servidor' registrado no Name Server!")
            logging.debug(f"[ESCUTANDO] Servidor registrado no Name Server e rodando na porta {self.porta}")
            
            self.daemon.requestLoop()
            
        except KeyboardInterrupt:
            logging.debug("\n[DESLIGANDO] Servidor parado pelo usuário.")
        except Exception as e:
            logging.error(f"[ERRO CRÍTICO] Falha na execução da rede: {e}")
            raise e
        finally:
            if self.daemon:
                self.daemon.close()
                logging.info("[DESLIGADO] Daemon do Pyro5 fechado com sucesso.")
        # try:
        #     while True:
        #         socket_cliente, endereco = self.servidor.accept()
        #         handler = ClientHandler(self.server_controller) 
        #         thread = threading.Thread(target=handler.handle_client, args=(socket_cliente, endereco))
        #         thread.start()
        #         logging.debug(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")
        # except KeyboardInterrupt:
        #     logging.debug("\n[DESLIGANDO] Servidor parado pelo usuário.")
        # finally:
        #     if self.servidor:
        #         self.servidor.close()
