from model.modelo_usuario import UsuarioModelo
from view.response_view import ResponseView

class AuthController:
    def register(self, message: dict) -> dict:
        data = message.get("data", {})
        nome_usuario = data.get("nomeUsuario")
        senha_usuario = data.get("senhaUsuario")

        if not nome_usuario or not senha_usuario:
            return ResponseView.error("INVALID_REGISTER", "Usuário e senha são obrigatórios.")

        sucesso, msg = UsuarioModelo.inserir(nome_usuario, senha_usuario)
        
        if sucesso:
            return ResponseView.success("REGISTER_RESPONSE", {"mensagem": msg})
        else:
            return ResponseView.error("INVALID_REGISTER", msg)

    def login(self, message: dict) -> dict:
        data = message.get("data", {})
        nome_usuario = data.get("nomeUsuario")
        senha_usuario = data.get("senhaUsuario")
        sala = data.get("sala") 

        if not nome_usuario or not senha_usuario:
            return ResponseView.error("INVALID_LOGIN", "Usuário e senha são obrigatórios.")

        usuario = UsuarioModelo.buscar_por_credenciais(nome_usuario, senha_usuario)
        
        if usuario:
            return ResponseView.success("LOGIN_RESPONSE", {
                "idUsuario": usuario[0], 
                "nomeUsuario": usuario[1],
                "sala": sala,
                "mensagem": "Login realizado com sucesso!"
            })
        else:
            return ResponseView.error("INVALID_LOGIN", "Credenciais inválidas ou usuário não encontrado.")