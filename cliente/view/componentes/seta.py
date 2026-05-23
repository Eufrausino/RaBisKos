from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint, QRectF
from .formas import Forma 
import math

class Seta(Forma):
    def __init__(self, x, y, cor, direcao="H",tamanho=80):
        super().__init__(x, y, cor)
        self.direcao = direcao #NOTE: "H" (Horizontal), "V" (Vertical), "D" (Diagonal)
        self.tamanho = tamanho

    def desenhar(self, painter:QPainter):
        painter.setPen(QPen(self.cor, 3))
        x1, y1 = self.x, self.y
        x2, y2 = x1, y1
        
        if self.direcao == "DIR": x2 += self.tamanho
        elif self.direcao == "ESQ": x2 -= self.tamanho
        elif self.direcao == "BAIXO": y2 += self.tamanho
        elif self.direcao == "CIMA": y2 -= self.tamanho
        elif self.direcao == "D_ID": x2 += self.tamanho * 0.7; y2 += self.tamanho * 0.7
        elif self.direcao == "D_SE": x2 -= self.tamanho * 0.7; y2 -= self.tamanho * 0.7
        elif self.direcao == "D_SD": x2 += self.tamanho * 0.7; y2 -= self.tamanho * 0.7
        elif self.direcao == "D_IE": x2 -= self.tamanho * 0.7; y2 += self.tamanho * 0.7
            
        #NOTE: Desenha Linha Principal
        painter.drawLine(x1, y1, int(x2), int(y2))
        
        #NOTE: Desenha a Ponta
        angulo = math.atan2(y2 - y1, x2 - x1)
        tamanho_ponta = 15
        abertura = math.pi / 6
        
        p1x = x2 - tamanho_ponta * math.cos(angulo - abertura)
        p1y = y2 - tamanho_ponta * math.sin(angulo - abertura)
        p2x = x2 - tamanho_ponta * math.cos(angulo + abertura)
        p2y = y2 - tamanho_ponta * math.sin(angulo + abertura)
        
        painter.drawLine(int(x2), int(y2), int(p1x), int(p1y))
        painter.drawLine(int(x2), int(y2), int(p2x), int(p2y))

    def contem_ponto(self, p):
        #NOTE: Para facilitar o arraste, verificamos se o clique está perto do início da seta
        return self.caixa_contorno().contains(p.x(), p.y())

    def caixa_contorno(self):
        x1, y1 = self.x, self.y
        x2, y2 = x1, y1
        if self.direcao == "DIR": x2 += self.tamanho
        elif self.direcao == "ESQ": x2 -= self.tamanho
        elif self.direcao == "BAIXO": y2 += self.tamanho
        elif self.direcao == "CIMA": y2 -= self.tamanho
        elif self.direcao == "D_ID": x2 += self.tamanho * 0.7; y2 += self.tamanho * 0.7
        elif self.direcao == "D_SE": x2 -= self.tamanho * 0.7; y2 -= self.tamanho * 0.7
        elif self.direcao == "D_SD": x2 += self.tamanho * 0.7; y2 -= self.tamanho * 0.7
        elif self.direcao == "D_IE": x2 -= self.tamanho * 0.7; y2 += self.tamanho * 0.7
        
        #NOTE: Cria um retângulo que engloba o ponto inicial e final, com uma margem (+- 15)
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)
        return QRectF(x_min - 15, y_min - 15, x_max - x_min + 30, y_max - y_min + 30)

