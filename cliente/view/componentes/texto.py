from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint, QRectF
from .formas import Forma

class Texto(Forma):
    def __init__(self, x, y, texto, tamanho_fonte, cor):
        super().__init__(x, y, cor)
        self.texto = texto
        self.tamanho_fonte = tamanho_fonte

    def desenhar(self, painter: QPainter):
        painter.setPen(QPen(self.cor))
        fonte = painter.font()
        fonte.setPointSize(self.tamanho_fonte)
        painter.setFont(fonte)
        
        painter.drawText(self.x, self.y, self.texto)

    def contem_ponto(self, p):
        #NOTE: Estimativa do tamanho da caixa de texto
        largura_estimada = len(self.texto) * (self.tamanho_fonte * 0.7)
        altura_estimada = self.tamanho_fonte * 1.2
        
        rect = QRectF(self.x, self.y - altura_estimada, largura_estimada, altura_estimada)
        return rect.contains(p.x(), p.y())
