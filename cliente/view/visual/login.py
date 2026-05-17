from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

class PaginaLogin(QWidget):
    solicitar_login = pyqtSignal(str,str,str)
    payload_registro = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_titulo = QLabel("Login")
        self.input_usuario = QLineEdit(placeholderText="Usuário")
        self.input_senha = QLineEdit(placeholderText="Senha")
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_sala = QLineEdit(placeholderText='ID Sala para Quadro Colaborativo')

        self.btn_entrar = QPushButton("Entrar")
        self.btn_entrar.clicked.connect(self.ao_clicar_login)

        self.btn_registrar = QPushButton("Criar nova conta")
        self.btn_registrar.setStyleSheet("border: none; color: blue; text-decoration: underline;")
        self.btn_registrar.clicked.connect(self.payload_registro.emit)

        layout.addWidget(self.label_titulo)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_senha)
        layout.addWidget(self.input_sala)
        layout.addWidget(self.btn_entrar)
        layout.addWidget(self.btn_registrar)
        
        self.setLayout(layout)

    def ao_clicar_login(self):
        usuario = self.input_usuario.text()
        senha = self.input_senha.text()
        sala = self.input_sala.text()
        self.solicitar_login.emit(usuario, senha, sala)
