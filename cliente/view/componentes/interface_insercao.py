from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint, QRectF
import math

class Interface_Insercao:
    @staticmethod
    def desenhar(painter: QPainter, tipo: str, x: int, y: int, w: int, h: int, cor: QColor, x2: int = None, y2: int = None):
        painter.setPen(QPen(cor, 3, Qt.PenStyle.SolidLine))
        
        if tipo == "LIVRE":
            # Aqui recuperamos a funcionalidade original: desenha do ponto A ao B
            if x2 is not None and y2 is not None:
                painter.drawLine(x, y, x2, y2)

        elif tipo == "QUADRILATERO":
            painter.drawRect(int(x - w/2), int(y - h/2), w, h)
            
        elif tipo == "CIRCULO":
            painter.drawEllipse(int(x - w/2), int(y - h/2), w, h)
            
        elif tipo == "LINHA_FIXA":
            # Caso o usuário queira "carimbar" uma linha de tamanho padrão
            painter.drawLine(x - 50, y, x + 50, y)
            
        elif tipo == "SETA":
            Interface_Insercao._desenhar_seta(painter, x - 50, y, x + 50, y)

    @staticmethod
    def _desenhar_seta(painter, x1, y1, x2, y2):
        # Corpo da seta
        painter.drawLine(x1, y1, x2, y2)
        
        # Lógica da ponta (Trigonometria)
        angulo = math.atan2(y2 - y1, x2 - x1)
        tamanho_ponta = 15
        abertura = math.pi / 6 # 30 graus
        
        px1 = x2 - tamanho_ponta * math.cos(angulo - abertura)
        py1 = y2 - tamanho_ponta * math.sin(angulo - abertura)
        px2 = x2 - tamanho_ponta * math.cos(angulo + abertura)
        py2 = y2 - tamanho_ponta * math.sin(angulo + abertura)
        
        painter.drawLine(x2, y2, int(px1), int(py1))
        painter.drawLine(x2, y2, int(px2), int(py2))
