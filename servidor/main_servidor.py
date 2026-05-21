import logging
from view.rede_servidor import ServidorRede

def principal():
    """
    Ponto de entrada do Servidor.
    Apenas instancia o Modelo de Rede e inicia o serviço.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    servidor = ServidorRede(host='0.0.0.0', porta=5000)
    servidor.iniciar()

if __name__ == "__main__":
    principal()

