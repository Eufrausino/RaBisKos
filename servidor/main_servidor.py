from view.rede_servidor import ServidorRede

def principal():
    """
    Ponto de entrada do Servidor.
    Apenas instancia o Modelo de Rede e inicia o serviço.
    """
    servidor = ServidorRede(host='0.0.0.0', porta=5000)
    servidor.iniciar()

if __name__ == "__main__":
    principal()

