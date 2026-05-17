from controller.auth_controller import AuthController
from controller.board_controller import BoardController
from controller.connection_manager import ConnectionManager
from controller.element_controller import ElementController
from view.response_view import ResponseView 

class ServerController:
    def __init__(self):
        self.auth_controller = AuthController()
        self.board_controller = BoardController()
        self.connection_manager = ConnectionManager()
        self.element_controller = ElementController(self.connection_manager)

    def handle_message(self, client_socket, message: dict) -> dict | None:
        tipo = message.get("type")
        
        if tipo == "PING":
            return ResponseView.success("PONG")
            
        elif tipo == "REGISTER":
            return self.auth_controller.register(message)
        elif tipo == "LOGIN":
            return self.auth_controller.login(message)

        elif tipo == "CREATE_QUADRO":
            resposta = self.board_controller.create_board(message)
            if resposta.get("status") == "ok":
                id_quadro = resposta["data"]["idQuadro"]
                self.connection_manager.add_client(id_quadro, client_socket)
            return resposta
            
        elif tipo == "JOIN_QUADRO":
            resposta = self.board_controller.join_board(message)
            if resposta.get("status") == "ok":
                id_quadro = resposta["data"]["idQuadro"]
                self.connection_manager.add_client(id_quadro, client_socket)
            return resposta
            
        elif tipo == "GET_QUADRO":
            return self.board_controller.get_board(message)
            
        elif tipo == "CREATE_ELEMENTO":
            return self.element_controller.create_element(message, client_socket)
        elif tipo == "UPDATE_ELEMENTO":
            return self.element_controller.update_element(message, client_socket)
        elif tipo == "DELETE_ELEMENTO":
            return self.element_controller.delete_element(message, client_socket)
            
        return ResponseView.error("INVALID_MESSAGE", "Tipo de comando desconhecido.")