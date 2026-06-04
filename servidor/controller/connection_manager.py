# import json
# import struct
import logging

class ConnectionManager:
    def __init__(self):
        self.salas = {}

    def add_client(self, id_quadro: int, client_callback) -> None:
        if id_quadro not in self.salas:
            self.salas[id_quadro] = []
            
        if client_callback not in self.salas[id_quadro]:
            self.salas[id_quadro].append(client_callback)
            logging.debug(f"[MANAGER] Cliente adicionado à sala {id_quadro}. Total na sala: {len(self.salas[id_quadro])}")

    def remove_client(self, client_callback) -> None:
        salas_a_remover = []
        for id_quadro, callbacks in self.salas.items():
            if client_callback in callbacks:
                callbacks.remove(client_callback)
                logging.debug(f"[MANAGER] Cliente removido da sala {id_quadro}")
  
            if not callbacks:
                salas_a_remover.append(id_quadro)
                
        for id_quadro in salas_a_remover:
            del self.salas[id_quadro]

    def broadcast_to_board(self, id_quadro: int, message: dict, exclude_callback=None) -> None:
        if id_quadro not in self.salas:
            return

        # dados_resposta = json.dumps(message).encode('utf-8')
        # cabecalho_resposta = struct.pack('>I', len(dados_resposta))
        # pacote = cabecalho_resposta + dados_resposta

        callbacks_falhos = []
        for client_callback in self.salas[id_quadro]:
            if client_callback != exclude_callback:
                try:
                    client_callback.notificar_evento(message)
                except Exception as e:
                    logging.debug(f"[MANAGER] Erro ao enviar broadcast para um cliente: {e}")
                    callbacks_falhos.append(client_callback)

        for falho in callbacks_falhos:
            self.remove_client(falho)
