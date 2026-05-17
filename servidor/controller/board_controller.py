from model.modelo_quadro import QuadroModelo
from model.modelo_usuario_quadro import UsuarioQuadroModelo
from view.response_view import ResponseView

class BoardController:
    def create_board(self, message: dict) -> dict:
        data = message.get("data", {})
        id_usuario_dono = data.get("idUsuarioDono")

        if not id_usuario_dono:
            return ResponseView.error("ERROR_CREATE_QUADRO", "ID do usuário dono é obrigatório.")
        
        sucesso, resultado = QuadroModelo.inserir(id_usuario_dono)
        
        if sucesso:
            id_quadro_sala = resultado
            
            sucesso_busca, quadro = QuadroModelo.buscar_quadro_por_idQuadroSala(id_quadro_sala)
            if sucesso_busca:
                UsuarioQuadroModelo.inserir(id_usuario_dono, quadro['IdQuadro'])
                
            return ResponseView.success("CREATE_BOARD_RESPONSE", {
                "idQuadroSala": id_quadro_sala,
                "idQuadro": quadro['IdQuadro'] if sucesso_busca else None
            })
        else:
            return ResponseView.error("ERROR_CREATE_QUADRO", resultado)

    def join_board(self, message: dict) -> dict:
        data = message.get("data", {})
        id_usuario = data.get("idUsuario")
        id_quadro_sala = data.get("idQuadroSala")

        sucesso, quadro = QuadroModelo.buscar_quadro_por_idQuadroSala(id_quadro_sala)
        
        if sucesso:
            id_quadro = quadro['IdQuadro']

            if id_usuario:
                UsuarioQuadroModelo.inserir(id_usuario, id_quadro)
                
            return ResponseView.success("JOIN_BOARD_RESPONSE", {
                "idQuadro": id_quadro,
                "idQuadroSala": id_quadro_sala
            })
        else:
            return ResponseView.error("BOARD_NOT_FOUND", "A sala informada não foi encontrada.")

    def get_board(self, message: dict) -> dict:
        data = message.get("data", {})
        id_quadro = data.get("idQuadro")

        if not id_quadro:
            return ResponseView.error("ERROR_GET_QUADRO", "ID do quadro é obrigatório.")

        return ResponseView.success("GET_BOARD_RESPONSE", {
            "idQuadro": id_quadro,
            "elementos": [] 
        })