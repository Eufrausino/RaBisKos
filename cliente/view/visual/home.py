from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class PaginaHome(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Estilo da tela em branco com o texto centralizado
        self.texto = QLabel("Seu SD aqui")
        self.texto.setStyleSheet("font-size: 32px; font-weight: bold; color: #34495e;")
        
        layout.addWidget(self.texto)
        self.setLayout(layout)
