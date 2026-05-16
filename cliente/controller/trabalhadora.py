from PyQt6.QtCore import QThread, pyqtSignal

class Worker(QThread):
    """
    Worker genérico para executar requisições de rede em background
    sem travar a interface gráfica (UI Thread).
    """
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
            self.deleteLater() # Garante a limpeza da memória após terminar
