import socket
import json
import struct

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
            print(f"Erro de conexão: {e}")
            return False

    def enviar_requisicao(self, tipo_requisicao, payload):
        if not self.socket:
            if not self.conectar():
                return {"sucesso": False, "mensagem": "Não foi possível conectar ao servidor"}
        
        try:
            requisicao = {
                "type": tipo_requisicao,
                "payload": payload
            }
            dados = json.dumps(requisicao).encode('utf-8')
            cabecalho = struct.pack('>I', len(dados))
            self.socket.sendall(cabecalho + dados)
            
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
            return {
                "sucesso": resposta.get('success', False),
                "mensagem": resposta.get('message', '')
            }
        except Exception as e:
            self.socket = None 
            return {"sucesso": False, "mensagem": f"Erro de rede: {e}"}

    def fechar(self):
        if self.socket:
            self.socket.close()
            self.socket = None
