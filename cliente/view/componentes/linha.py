from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint, QRectF
from .formas import Forma
import math

class Linha(Forma):
    def __init__(self, cor):
        super().__init__(0, 0, cor) # Posição inicial relativa
        self.pontos = [] # Lista de QPoint

    def desenhar(self, painter):
        if len(self.pontos) < 2: return
        painter.setPen(QPen(self.cor, 3))
        for i in range(len(self.pontos) - 1):
            painter.drawLine(self.pontos[i], self.pontos[i+1])

    def contem_ponto(self, p):
        #NOTE: Estimativa para pegar todos os pontos
        for ponto in self.pontos:
            if math.hypot(p.x() - ponto.x(), p.y() - ponto.y()) < 20:
                return True
        return False

    def mover(self, dx, dy):
        for i in range(len(self.pontos)):
            p = self.pontos[i]
            self.pontos[i] = QPoint(p.x() + dx, p.y() + dy)
        self.x += dx
        self.y += dy

    def caixa_contorno(self):
        if not self.pontos: return QRectF(self.x, self.y, 0, 0)
        xs = [p.x() for p in self.pontos]
        ys = [p.y() for p in self.pontos]
        return QRectF(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
