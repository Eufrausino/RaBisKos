import sys
from PyQt6.QtWidgets import QApplication
from view.visual.principal import JanelaPrincipal
from controller.controladora_client import ControladorCliente

def principal():
    app = QApplication(sys.argv)
    
    # Inicializar View
    janela = JanelaPrincipal()
    
    # Inicializar Controller (ele cria o Model internamente)
    # controlador = ControladorCliente(janela)
    
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    principal()
