# import json
# import struct
import logging
import Pyro5.api

class ConnectionManager:
    def __init__(self):
        # Agora armazenamos URIs (strings) em vez de objetos Proxy
        self.salas = {}

    def _get_uri(self, callback):
        """Função auxiliar para extrair a URI de forma segura"""
        if hasattr(callback, '_pyroUri'):
            return str(callback._pyroUri)
        return str(callback)

    def add_client(self, id_quadro: int, client_callback) -> None:
        if id_quadro not in self.salas:
            self.salas[id_quadro] = []
            
        # Extrai a URI do callback para evitar problemas de thread
        uri = self._get_uri(client_callback)
        
        if uri not in self.salas[id_quadro]:
            self.salas[id_quadro].append(uri)
            logging.debug(f"[MANAGER] Cliente adicionado à sala {id_quadro}. Total na sala: {len(self.salas[id_quadro])}")

    def remove_client(self, client_callback) -> None:
        uri_to_remove = self._get_uri(client_callback)
        salas_a_remover = []
        
        for id_quadro, uris in self.salas.items():
            if uri_to_remove in uris:
                uris.remove(uri_to_remove)
                logging.debug(f"[MANAGER] Cliente removido da sala {id_quadro}")
  
            if not uris:
                salas_a_remover.append(id_quadro)
                
        for id_quadro in salas_a_remover:
            del self.salas[id_quadro]

    def broadcast_to_board(self, id_quadro: int, message: dict, exclude_callback=None) -> None:
        if id_quadro not in self.salas:
            return

        exclude_uri = self._get_uri(exclude_callback) if exclude_callback else None
        uris_falhas = []
        
        for uri in self.salas[id_quadro]:
            if uri != exclude_uri:
                try:
                    #NOTE: Cria um novo proxy na thread atual usando a URI
                    with Pyro5.api.Proxy(uri) as client_proxy:
                        client_proxy.notificar_evento(message)
                except Exception as e:
                    logging.debug(f"[MANAGER] Erro ao enviar broadcast para um cliente: {e}")
                    uris_falhas.append(uri) #NOTE: Passa a URI para remoção

        for falha_uri in uris_falhas:
            self.remove_client(falha_uri)