from PyQt6.QtWidgets import QMainWindow, QWidget, QToolBar
from PyQt6.QtGui import QPainter, QPen, QImage, QColor
from PyQt6.QtCore import Qt, QPoint, pyqtSignal

class JanelaPrincipal(QMainWindow):
    #NOTE:QUADRO BRANCO

    #NOTE:INDICA ULTIMA_POS_X, ULTIMA_POS_Y, POS_ATUAL_X, POS_ATUAL_Y e COR
    ponto_desenhado = pyqtSignal(int, int, int, int,str)
    def __init__(self):
        super().__init__()
        #NOTE: Permite mudar de cor - qt faz perder foco quando interage com outro widget
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setWindowTitle("Quadro Branco")
        
        self.container = QWidget()
        self.setCentralWidget(self.container)
        
        self.image = QImage(800, 600, QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)
        
        #NOTE: Onde vai ter a parte de funcionalidades
        #TODO: Add elementos, Gerar número sala, borracha
        self.toolbar = QToolBar("Ferramentas")
        self.addToolBar(self.toolbar)
        self.toolbar.addAction("Limpar", self.limpar_quadro)
        #self.toolbar.addAction("Inserir Elemento", self.adicionar_elemento)
        
        #NOTE: Utilitário do qt para verificar posição
        self.ultima_posicao = QPoint()
        #NOTE: Define cor default como preto
        self.cor_atual = QColor(Qt.GlobalColor.black)
        #NOTE: FOCA
        self.setFocus()

    #NOTE: Captura as teclas para mudar cor
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_1:
            self.cor_atual = QColor(Qt.GlobalColor.red)
        elif event.key() == Qt.Key.Key_2:
            self.cor_atual = QColor(Qt.GlobalColor.blue)
        elif event.key() == Qt.Key.Key_3:
            self.cor_atual = QColor(Qt.GlobalColor.green)
        elif event.key() == Qt.Key.Key_0:
            self.cor_atual = QColor(Qt.GlobalColor.black)
        
    def limpar_quadro(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.ultima_posicao = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            posicao_atual = event.position().toPoint()
            self.desenhar_linha(self.ultima_posicao, posicao_atual,self.cor_atual)
            cor = QColor(self.cor_atual).name()
            
            self.ponto_desenhado.emit(self.ultima_posicao.x(), self.ultima_posicao.y(),
            posicao_atual.x(), posicao_atual.y(), cor)
            
            self.ultima_posicao = posicao_atual

    def desenhar_linha(self, inicio, fim,cor):
        painter = QPainter(self.image)
        painter.setPen(QPen(cor, 3, Qt.PenStyle.SolidLine))
        painter.drawLine(inicio, fim)
        painter.end()
        self.update()

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def resizeEvent(self, event):
        if self.image.size() != self.size():
            nova_imagem = QImage(self.size(), QImage.Format.Format_RGB32)
            nova_imagem.fill(Qt.GlobalColor.white)
            
            painter = QPainter(nova_imagem)
            painter.drawImage(QPoint(0, 0), self.image)
            painter.end()
            
            self.image = nova_imagem
        super().resizeEvent(event)
