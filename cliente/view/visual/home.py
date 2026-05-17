from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from .registro import PaginaRegistro
from .login import PaginaLogin
from .principal import JanelaPrincipal

class JanelaNavegacao(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RaBisKos")
        self.setFixedSize(850, 650)

        self.stack = QStackedWidget()
        
        self.pagina_login = PaginaLogin()
        self.pagina_registro = PaginaRegistro()
        self.pagina_principal = JanelaPrincipal()

        self.stack.addWidget(self.pagina_login)    
        self.stack.addWidget(self.pagina_registro) 
        self.stack.addWidget(self.pagina_principal)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.stack)

        container = QWidget()
        container.setLayout(layout_principal)
        self.setCentralWidget(container)

        # (Login -> Registro)
        self.pagina_login.payload_registro.connect(lambda: self.mudar_pagina(1))
        self.pagina_registro.dados_registro.connect(lambda: self.mudar_pagina(0))

    def mudar_pagina(self, indice):
        self.stack.setCurrentIndex(indice)

    def obter_indice_atual(self):
        return self.stack.currentIndex()

    def definir_carregamento(self, ativo):
        self.stack.setEnabled(not ativo)
