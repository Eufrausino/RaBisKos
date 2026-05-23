from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint, QRectF
from abc import ABC, abstractmethod

#NOTE: Classe abstrata -> componentes específicos herdam atributos e implementam métodos
class Forma:
    #NOTE: posições x,y; largura; altura e cor
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = QColor(cor)
        self.selecionada = False
        self.id_elemento = None  

    #NOTE: Desenha
    @abstractmethod
    def desenhar(self, painter: QPainter):
        pass

    #NOTE: Confere se já tem algo desenhado no ponto - serve para seleção do elemento 
    @abstractmethod
    def contem_ponto(self, ponto: QPoint) -> bool:
        pass
    
    #NOTE: Demarca área de seleção
    @abstractmethod
    def caixa_contorno(self) -> QRectF:
        pass
