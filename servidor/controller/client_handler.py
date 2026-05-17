import struct
import json

class ClientHandler:
    def __init__(self, server_controller): 
        self.server_controller = server_controller

    def handle_client(self, client_socket, endereco) -> None:
        print(f"[NOVA LIGAÇÃO] {endereco} conectado.")
        try:
            while True:
                mensagem = self.receive_message(client_socket)
                if not mensagem:
                    break 
                
                print(f"[REQUISIÇÃO] {mensagem.get('type')} de {endereco}")
                
                resposta = self.server_controller.handle_message(client_socket, mensagem)

                if resposta:
                    self.send_response(client_socket, resposta)
                    
        except Exception as e:
            print(f"[ERRO] {endereco}: {e}")
        finally:
            if hasattr(self.server_controller, 'connection_manager'):
                self.server_controller.connection_manager.remove_client(client_socket)
            
            client_socket.close()
            print(f"[DESCONECTADO] {endereco} fechado.")

    def receive_message(self, client_socket) -> dict:
        cabecalho = client_socket.recv(4)
        if not cabecalho:
            return None
        
        tamanho_mensagem = struct.unpack('>I', cabecalho)[0]
        
        dados = b''
        while len(dados) < tamanho_mensagem:
            chunk = client_socket.recv(tamanho_mensagem - len(dados))
            if not chunk:
                return None
            dados += chunk

        return json.loads(dados.decode('utf-8'))

    def send_response(self, client_socket, response: dict) -> None:
        dados_resposta = json.dumps(response).encode('utf-8')
        cabecalho_resposta = struct.pack('>I', len(dados_resposta))
        client_socket.sendall(cabecalho_resposta + dados_resposta)