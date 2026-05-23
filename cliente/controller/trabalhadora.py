from PyQt6.QtCore import QThread, pyqtSignal

class Worker(QThread):
    sinal_resultado = pyqtSignal(dict)
    sinal_erro = pyqtSignal(str)
    
    def __init__(self, cliente, tipo_requisicao, payload):
        super().__init__()
        self.cliente = cliente
        self.tipo_requisicao = tipo_requisicao
        self.payload = payload
        
    def run(self):
        try:
            resposta = self.cliente.enviar_requisicao(self.tipo_requisicao, self.payload)
            self.sinal_resultado.emit(resposta)
        except Exception as e:
            self.sinal_erro.emit(str(e))
        finally:
            self.deleteLater() 

class ThreadEscuta(QThread):
    sinal_evento = pyqtSignal(dict)
    
    def __init__(self, cliente):
        super().__init__()
        self.cliente = cliente
        self.rodando = True
        
    def run(self):
        while self.rodando:
            mensagem = self.cliente.escutar_servidor()
            if mensagem:
                self.sinal_evento.emit(mensagem)
            else:
                self.rodando = False 