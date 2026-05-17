import sys
from PyQt6.QtWidgets import QApplication
from view.visual.home import JanelaNavegacao
from controller.controladora_client import ControladorCliente

def principal():
    app = QApplication(sys.argv)
    
    janela = JanelaNavegacao()
    
    controlador = ControladorCliente(janela)
    
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    principal()
