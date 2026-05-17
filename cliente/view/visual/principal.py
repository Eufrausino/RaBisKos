from PyQt6.QtWidgets import QMainWindow, QWidget, QToolBar
from PyQt6.QtGui import QPainter, QPen, QImage
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from view.visual.registro import PaginaRegistro

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quadro Branco")
        
        self.container = QWidget()
        self.setCentralWidget(self.container)
        
        self.image = QImage(800, 600, QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)
        
        self.toolbar = QToolBar("Ferramentas")
        self.addToolBar(self.toolbar)
        self.toolbar.addAction("Limpar", self.limpar_quadro)
        
    def limpar_quadro(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            posicao_atual = event.position().toPoint()
            self.desenhar_linha(self.ultima_posicao, posicao_atual)
            
            self.ponto_desenhado.emit(self.ultima_posicao.x(), self.ultima_posicao.y(),
            posicao_atual.x(), posicao_atual.y())
            
            self.ultima_posicao = posicao_atual

    def desenhar_linha(self, inicio, fim):
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.GlobalColor.black, 3, Qt.PenStyle.SolidLine))
        painter.drawLine(inicio, fim)
        self.update()

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())
