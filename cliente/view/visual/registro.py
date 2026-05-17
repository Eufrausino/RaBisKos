from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

class PaginaRegistro(QWidget):
    dados_registro = pyqtSignal(str,str)
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Página de Registro")
        self.setMinimumWidth(400)
        self.setMaximumHeight(400)

        self.estrutura_UI()

    def estrutura_UI(self):
        layout = QVBoxLayout()
        
        self.label_titulo = QLabel("Tela de Registro")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_titulo)

        self.label_usuario = QLabel("Nome de Usuário:")
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Digite seu usuário...")
        
        layout.addWidget(self.label_usuario)
        layout.addWidget(self.input_usuario)

        self.label_senha = QLabel("Senha:")
        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Digite sua senha...")
        #NOTE: Senha fica ..... e não a string na tela do usuário
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)         
        layout.addWidget(self.label_senha)
        layout.addWidget(self.input_senha)

        
        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_registrar.clicked.connect(self.ao_registrar)
        layout.addWidget(self.btn_registrar)

        self.setLayout(layout)

    #NOTE: Entrada/Input de dados e sinal para servidor
    def ao_registrar(self):
        usuario = self.input_usuario.text()
        senha = self.input_senha.text()
        
        if usuario and senha:
            print(f"Tentativa de registro: Usuário='{usuario}', Senha='{senha}'")
            self.dados_registro.emit(usuario, senha)
        else:
            QMessageBox.warning(self, "Erro", "Preencha usuário e senha!")
