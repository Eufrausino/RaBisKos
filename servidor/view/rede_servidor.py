import socket
import threading
import logging
from model.banco_de_dados.banco import inicializar_banco
from controller.client_handler import ClientHandler
from controller.server_controller import ServerController

class ServidorRede:
    """
    Camada de Visão (Interface) do Servidor.
    Responsável por gerenciar conexões TCP, threads e o protocolo de comunicação.
    """
    
    def __init__(self, host='0.0.0.0', porta=5000):
        self.host = host
        self.porta = porta
        self.servidor = None
        self.server_controller = ServerController()

    def iniciar(self):
        inicializar_banco()
        
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servidor.bind((self.host, self.porta))
        self.servidor.listen()
        
        logging.debug(f"[ESCUTANDO] Servidor MVC rodando em {self.host}:{self.porta}")
        
        try:
            while True:
                socket_cliente, endereco = self.servidor.accept()
                handler = ClientHandler(self.server_controller) 
                thread = threading.Thread(target=handler.handle_client, args=(socket_cliente, endereco))
                thread.start()
                logging.debug(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")
        except KeyboardInterrupt:
            logging.debug("\n[DESLIGANDO] Servidor parado pelo usuário.")
        finally:
            if self.servidor:
                self.servidor.close()