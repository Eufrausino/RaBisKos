from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QRectF
from .formas import Forma

class Retangulo(Forma):
    def __init__(self, x, y, w, h, cor):
        super().__init__(x, y, cor)
        self.w = w
        self.h = h

    def desenhar(self, painter: QPainter):
        painter.setPen(QPen(self.cor, 3, Qt.PenStyle.SolidLine))
        #NOTE: desenha a partir do centro do clique
        painter.drawRect(int(self.x - self.w/2), int(self.y - self.h/2), self.w, self.h)

    def contem_ponto(self, p):
        rect = QRectF(self.x - self.w/2, self.y - self.h/2, self.w, self.h)
        return rect.contains(p.x(), p.y())

    def caixa_contorno(self):
        return QRectF(self.x - self.w/2, self.y - self.h/2, self.w, self.h)

