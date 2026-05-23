import socket
import json
import struct
import logging

#template
class ClienteRede:
    def __init__(self, host='localhost', porta=5000):
        self.host = host
        self.porta = porta
        self.socket = None

    def conectar(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.porta))
            return True
        except Exception as e:
            logging.debug(f"Erro de conexão: {e}")
            return False

    def enviar_requisicao(self, tipo_requisicao, payload, esperar_resposta=True):
        if not self.socket:
            if not self.conectar():
                return {"sucesso": False, "mensagem": "Não foi possível conectar ao servidor"}
        
        try:
            requisicao = {
                "type": tipo_requisicao,
                #mudei aqui gustavo, antes era "payload" no lugar de "data"
                "data": payload
            }
            dados = json.dumps(requisicao).encode('utf-8')
            cabecalho = struct.pack('>I', len(dados))
            self.socket.sendall(cabecalho + dados)

            if not esperar_resposta:
                return {"sucesso": True, "mensagem": "Enviado"}
            
            # Ler resposta
            cabecalho = self.socket.recv(4)
            if not cabecalho:
                return {"sucesso": False, "mensagem": "Servidor fechou a conexão"}
            
            tamanho_mensagem = struct.unpack('>I', cabecalho)[0]
            dados = b''
            while len(dados) < tamanho_mensagem:
                chunk = self.socket.recv(tamanho_mensagem - len(dados))
                if not chunk:
                    break
                dados += chunk
            
            resposta = json.loads(dados.decode('utf-8'))
            # mudei aqui gustavo. acrescentei as 5 linhas de baixo antes de return. 
            sucesso = resposta.get('status') == 'ok'
            if sucesso:
                mensagem = resposta.get('data', {}).get('mensagem', '')
            else:
                mensagem = resposta.get('message', '')
            return {
                # "sucesso": resposta.get('success', False),
                # "mensagem": resposta.get('message', '')

                # mudei aqui gustavo.
                "sucesso": sucesso,
                "mensagem": mensagem,
                "dados": resposta.get('data', {})
            }
        except Exception as e:
            self.socket = None 
            return {"sucesso": False, "mensagem": f"Erro de rede: {e}"}

    def fechar(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def escutar_servidor(self):
        try:
            cabecalho = self.socket.recv(4)
            if not cabecalho:
                return None
            
            tamanho_mensagem = struct.unpack('>I', cabecalho)[0]
            dados = b''
            while len(dados) < tamanho_mensagem:
                chunk = self.socket.recv(tamanho_mensagem - len(dados))
                if not chunk:
                    return None
                dados += chunk
            
            return json.loads(dados.decode('utf-8'))
        except Exception:
            return None
