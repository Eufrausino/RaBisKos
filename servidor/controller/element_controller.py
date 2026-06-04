# import dataclasses
import logging
from model.modelo_elemento import ElementoModelo
from view.response_view import ResponseView

class ElementController:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    def create_element(self, message: dict, client_callback) -> dict:
        data = message.get("data", {})

        logging.debug(f"[DEBUG] JSON recebido pelo servidor: {data}")
        if 'texto' in data:
            logging.debug(f"[DEBUG] Sucesso: Texto '{data['texto']}' recebido")
        else:
            logging.debug(f"[ERRO] O campo 'texto' não chegou ao servidor! Chaves recebidas: {list(data.keys())}")

        id_quadro = data.get("idQuadro")
        
        versao = data.get("versao", 1) 

        sucesso, msg = ElementoModelo.inserir(id_quadro, data, versao)
        
        if sucesso:
            # broadcast_msg = ResponseView.event("ELEMENT_CREATED", data)
            
            # logging.debug(f"[DEBUG SERVIDOR] Disparando broadcast para o quadro {id_quadro} com: {data.get('tipo')}")

            data["idElemento"] = msg
            broadcast_msg = ResponseView.event("ELEMENT_CREATED", data)
            logging.debug(f"[DEBUG SERVIDOR] Disparando broadcast para o quadro {id_quadro} com: {data.get('tipo')}")
            self.connection_manager.broadcast_to_board(id_quadro, broadcast_msg, exclude_callback=client_callback)
            
            return ResponseView.success("CREATE_ELEMENT_RESPONSE", {"idElemento": msg})
        else:
            return ResponseView.error("ERROR_CREATE_ELEMENTO", str(msg)) 
            #NOTE: adicionei typecast pq tipo da msg nao casava com o parametro do metodo (tlvz mudar no proprio metodo dps) segundo o interpretador python

    def update_element(self, message: dict, client_callback) -> dict:
        data = message.get("data", {})
        id_elemento = data.get("idElemento")
        id_quadro = data.get("idQuadro")
        versao = data.get("versao")

        sucesso, msg = ElementoModelo.atualizar(id_elemento, data, versao)
        
        if sucesso:
            broadcast_msg = ResponseView.event("ELEMENT_UPDATED", data)
            self.connection_manager.broadcast_to_board(id_quadro, broadcast_msg, exclude_callback=client_callback)
            
            return ResponseView.success("UPDATE_ELEMENT_RESPONSE", {"mensagem": msg})
        else:
            return ResponseView.error("ERROR_UPDATE_ELEMENTO", msg)

    def delete_element(self, message: dict, client_callback) -> dict:
        data = message.get("data", {})
        id_elemento = data.get("idElemento")
        id_quadro = data.get("idQuadro")

        sucesso, msg = ElementoModelo.remover(id_elemento)
        
        if sucesso:
            broadcast_msg = ResponseView.event("ELEMENT_DELETED", {
                "idQuadro": id_quadro,
                "idElemento": id_elemento
            })
            self.connection_manager.broadcast_to_board(id_quadro, broadcast_msg, exclude_callback=client_callback)
            
            return ResponseView.success("DELETE_ELEMENT_RESPONSE", {"mensagem": msg})
        else:
            return ResponseView.error("ERROR_DELETE_ELEMENTO", msg)
    
    def clear_board(self, message: dict, client_callback) -> dict:
        data = message.get("data", {})
        id_quadro = data.get("idQuadro")

        sucesso, msg = ElementoModelo.limpar_quadro(id_quadro)
        
        if sucesso:
            # Notifica todos na sala (exceto quem solicitou)
            broadcast_msg = ResponseView.event("BOARD_CLEARED", {
                "idQuadro": id_quadro
            })
            self.connection_manager.broadcast_to_board(id_quadro, broadcast_msg, exclude_callback=client_callback)
            
            return ResponseView.success("CLEAR_BOARD_RESPONSE", {"mensagem": msg})
        else:
            return ResponseView.error("ERROR_CLEAR_BOARD", msg)
  
