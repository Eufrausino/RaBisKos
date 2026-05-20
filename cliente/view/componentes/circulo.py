from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QRectF
from .formas import Forma
import math

class Circulo(Forma):
    def __init__(self, x, y, w, h, cor):
        super().__init__(x, y, cor)
        self.w = w
        self.h = h

    def desenhar(self, painter):
        painter.setPen(QPen(self.cor, 3, Qt.PenStyle.SolidLine))
        painter.drawEllipse(int(self.x - self.w/2), int(self.y - self.h/2), self.w, self.h)

    def contem_ponto(self, p):
        #NOTE: Distância Euclidiana para precisão no círculo -> seleção fica esquisita sem usar
        distancia = math.hypot(p.x() - self.x, p.y() - self.y)
        return distancia <= (self.w / 2)

    def caixa_contorno(self):
        return QRectF(self.x - self.w/2, self.y - self.h/2, self.w, self.h)
