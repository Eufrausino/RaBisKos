import json
import struct

class ConnectionManager:
    def __init__(self):
        self.salas = {}

    def add_client(self, id_quadro: int, client_socket) -> None:
        if id_quadro not in self.salas:
            self.salas[id_quadro] = []
            
        if client_socket not in self.salas[id_quadro]:
            self.salas[id_quadro].append(client_socket)
            print(f"[MANAGER] Cliente adicionado à sala {id_quadro}. Total na sala: {len(self.salas[id_quadro])}")

    def remove_client(self, client_socket) -> None:
        salas_a_remover = []
        for id_quadro, sockets in self.salas.items():
            if client_socket in sockets:
                sockets.remove(client_socket)
                print(f"[MANAGER] Cliente removido da sala {id_quadro}")
  
            if not sockets:
                salas_a_remover.append(id_quadro)
                
        for id_quadro in salas_a_remover:
            del self.salas[id_quadro]

    def broadcast_to_board(self, id_quadro: int, message: dict, exclude_socket=None) -> None:
        if id_quadro not in self.salas:
            return

        dados_resposta = json.dumps(message).encode('utf-8')
        cabecalho_resposta = struct.pack('>I', len(dados_resposta))
        pacote = cabecalho_resposta + dados_resposta

        sockets_falhos = []
        for client_socket in self.salas[id_quadro]:
            if client_socket != exclude_socket:
                try:
                    client_socket.sendall(pacote)
                except Exception as e:
                    print(f"[MANAGER] Erro ao enviar broadcast para um cliente: {e}")
                    sockets_falhos.append(client_socket)

        for falho in sockets_falhos:
            self.remove_client(falho)