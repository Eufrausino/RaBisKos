from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor

class PaginaRegistro(QWidget):
    dados_registro = pyqtSignal(str,str)
    voltar_login = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(15, 15, 15, 15)
        
        self.container = QFrame()
        self.container.setObjectName("container")
        
        layout_container = QVBoxLayout(self.container)
        layout_container.setSpacing(10)
        layout_container.setContentsMargins(20, 20, 20, 20)
        
        self.label_imagem = QLabel()
        pixmap = QPixmap("view/assets/logo.png").scaled(
            400, 400, 
            Qt.AspectRatioMode.KeepAspectRatio, 
        )
        self.label_imagem.setPixmap(pixmap)
        self.label_imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.input_usuario = QLineEdit(placeholderText="Usuário")
        self.input_senha = QLineEdit(placeholderText="Senha")
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.ao_registrar)
        
        self.btn_voltar = QPushButton("Voltar para Login")
        self.btn_voltar.setStyleSheet("border: none; color: blue; text-decoration: underline;")
        self.btn_voltar.clicked.connect(self.voltar_login.emit)
        
        layout_container.addWidget(self.label_imagem, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_container.addWidget(self.input_usuario, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_container.addWidget(self.input_senha, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_container.addWidget(self.btn_registrar, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_container.addWidget(self.btn_voltar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        efeito_sombra = QGraphicsDropShadowEffect(self)
        efeito_sombra.setBlurRadius(15)
        efeito_sombra.setXOffset(0)
        efeito_sombra.setYOffset(4)
        efeito_sombra.setColor(QColor(0, 0, 0, 50))
        self.container.setGraphicsEffect(efeito_sombra)
        
        self.setStyleSheet("""
            PaginaRegistro {
                background-color: #0F172A
            }
            QFrame#container {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            QLineEdit, QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #D1D5DB; 
                border-radius: 6px;       
                padding: 8px 12px;         
                font-size: 14px;
                color: #1F2937;    
                min-width: 250px;
                max-width: 250px;   
            }
            QLineEdit:hover, QPushButton:hover {
                background-color: #F3F4F6;
            }
        """)
        
        layout_principal.addStretch()
        layout_principal.addWidget(self.container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_principal.addStretch()
        
        self.setLayout(layout_principal)

    def ao_registrar(self):
        usuario = self.input_usuario.text()
        senha = self.input_senha.text()
        
        if usuario and senha:
            print(f"Tentativa de registro: Usuário='{usuario}', Senha='{senha}'")
            self.dados_registro.emit(usuario, senha)
        else:
            QMessageBox.warning(self, "Erro", "Preencha usuário e senha!")
