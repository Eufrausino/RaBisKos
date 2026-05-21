from PyQt6.QtWidgets import QMainWindow, QWidget, QToolBar, QPushButton, QMenu, QInputDialog, QToolButton, QLabel
from PyQt6.QtGui import QPainter, QPen, QImage, QColor
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QRectF
import json
from ..componentes import Retangulo, Circulo, Seta, Linha, Texto

class JanelaPrincipal(QMainWindow):
    #NOTE:QUADRO BRANCO

    #NOTE:INDICA COMPONENTE, ULTIMA_POS_X, ULTIMA_POS_Y, POS_ATUAL_X, POS_ATUAL_Y e COR
    ponto_desenhado = pyqtSignal(str,int, int, int, int,str)
    elemento_criado = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        #NOTE: Permite mudar de cor - qt faz perder foco quando interage com outro widget
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setWindowTitle("Quadro Branco")
        
        self.container = QWidget()
        self.setCentralWidget(self.container)
        
        self.image = QImage(800, 600, QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)

        self.elementos = []  #NOTE: lista de componentes
        self.elemento_selecionado = None #NOTE: serve para arrastar
        self.direcao_seta_atual = "H"

        self.toolbar = QToolBar("Ferramentas")
        self.addToolBar(self.toolbar)
        self.configurar_toolbar()

        self.ferramenta_ativa = "LIVRE" #NOTE: Desenhar é o default
        self.dimensoes = {"w": 100, "h": 100}
        
        #NOTE: Utilitário do qt para verificar posição
        self.ultima_posicao = QPoint()
        #NOTE: Define cor default como preto
        self.cor_atual = QColor(Qt.GlobalColor.black)
        #NOTE: ID da sala atual
        self.id_sala = None
        #NOTE: FOCA
        self.setFocus()

    #NOTE: Captura as teclas para mudar cor
    def keyPressEvent(self, event):
        tecla = event.text()
        nova_cor = None
        
        if tecla == '1':
            nova_cor = QColor(Qt.GlobalColor.red)
        elif tecla == '2':
            nova_cor = QColor(Qt.GlobalColor.blue)
        elif tecla == '3':
            nova_cor = QColor(Qt.GlobalColor.green)
        elif tecla == '0':
            nova_cor = QColor(Qt.GlobalColor.black)

        if nova_cor:
            self.cor_atual = nova_cor
            
            #NOTE: Seletor ativo permite mduar de cor
            if self.ferramenta_ativa == "MAO" and self.elemento_selecionado:
                self.elemento_selecionado.cor = nova_cor
                self.statusBar().showMessage(f"Elemento atualizado para a cor {tecla}")
            else:
                self.statusBar().showMessage(f"Cor do pincel alterada para a cor {tecla}")
                
            self.update()
        else:
            #NOTE: repassa o evento para frente se não for uma tecla de cor
            super().keyPressEvent(event)
            
        #NOTE: DELETE
        if event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
            if self.ferramenta_ativa == "MAO" and self.elemento_selecionado:
                self.elementos.remove(self.elemento_selecionado)
                self.elemento_selecionado = None
                self.statusBar().showMessage("Elemento deletado.")
                self.update()

    def limpar_quadro(self):
        self.elementos.clear() #NOTE: Esvazia a lista de componentes
        self.elemento_selecionado = None
        if hasattr(self, 'caminho_em_construcao'):
            self.caminho_em_construcao = None
        self.update() #NOTE: Redesenha a tela em branco

    def mousePressEvent(self, event):
        try:
            self.setFocus()
            if event.button() != Qt.MouseButton.LeftButton:
                return

            pos = event.position().toPoint()
            self.ultimo_ponto_mouse = pos 

            #NOTE: MODO SELEÇÃO E ARRASTE
            if self.ferramenta_ativa == "MAO":
                self.elemento_selecionado = None
                for elemento in reversed(self.elementos):
                    if elemento.contem_ponto(pos):
                        self.elemento_selecionado = elemento
                        self.statusBar().showMessage(f"Selecionado: {type(elemento).__name__}")
                        break
                        
                if not self.elemento_selecionado:
                    self.statusBar().showMessage("Modo: Mão (Nenhum elemento selecionado)")

            #NOTE: Componentes gráficos
            else:
                self.elemento_selecionado = None
                
                if self.ferramenta_ativa == "LIVRE":
                    self.caminho_em_construcao = Linha(self.cor_atual)
                    self.caminho_em_construcao.pontos.append(pos)
                    self.elementos.append(self.caminho_em_construcao)
                    
                elif self.ferramenta_ativa == "QUADRILATERO":
                    novo = Retangulo(pos.x(), pos.y(), self.dimensoes["w"], self.dimensoes["h"], self.cor_atual)
                    if self.espaco_livre(novo.caixa_contorno()):
                        self.elementos.append(novo)
                    else:
                        self.statusBar().showMessage("Espaço ocupado! Sobreposição não permitida.")
                        
                elif self.ferramenta_ativa == "CIRCULO":
                    novo = Circulo(pos.x(), pos.y(), self.dimensoes["w"], self.dimensoes["h"], self.cor_atual)
                    if self.espaco_livre(novo.caixa_contorno()):
                        self.elementos.append(novo)
                    else:
                        self.statusBar().showMessage("Espaço ocupado! Sobreposição não permitida.")
                        
                elif self.ferramenta_ativa == "TEXTO":
                    novo = Texto(pos.x(), pos.y(), self.dimensoes['w'], self.dimensoes['h'], self.texto_atual, self.tamanho_fonte_atual, self.cor_atual)
                    if self.espaco_livre(novo.caixa_contorno()):
                        self.elementos.append(novo)
                    else:
                        self.statusBar().showMessage("Espaço ocupado! Sobreposição não permitida.")

                elif self.ferramenta_ativa == "SETA":
                    tamanho = getattr(self, "tamanho_seta_atual", 80)
                    novo = Seta(pos.x(), pos.y(), self.cor_atual, self.direcao_seta_atual, tamanho)
                    if self.espaco_livre(novo.caixa_contorno()):
                        self.elementos.append(novo)
                    else:
                        self.statusBar().showMessage("Espaço ocupado! Sobreposição não permitida.")

            self.update()   
            
            if self.ferramenta_ativa not in ['MAO','LIVRE'] and self.elemento_selecionado is None:
                texto_envio = ""
                if self.ferramenta_ativa == "TEXTO":
                    texto_envio = getattr(self, "texto_atual", "Texto")
                elif self.ferramenta_ativa == "SETA":
                    texto_envio = getattr(self, "direcao_seta_atual", "DIR")

                largura_envio = self.dimensoes.get("w", 100)
                altura_envio = self.dimensoes.get("h", 100)
                
                if self.ferramenta_ativa == "SETA":
                    largura_envio = getattr(self, "tamanho_seta_atual", 80)
                elif self.ferramenta_ativa == "TEXTO":
                    altura_envio = getattr(self, "tamanho_fonte_atual", 24)

                dados = {
                    "tipo": self.mapear_tipo(self.ferramenta_ativa),
                    "posx": pos.x(),
                    "posy": pos.y(),
                    "largura": largura_envio,
                    "altura": altura_envio,
                    "cor": self.obter_codigo_cor(self.cor_atual),
                    "texto": texto_envio
                }
                self.elemento_criado.emit(dados)
                print(f"[DEBUG - DISPARANDO EMIT] {dados}")
        except Exception as e:
            print(f"ERRO CRÍTICO NO MOUSE PRESS: {e}")

    def mouseReleaseEvent(self, event):
        
        if event.button() == Qt.MouseButton.LeftButton:
            # Se for desenho livre e existir uma linha sendo construída
            if self.ferramenta_ativa == "LIVRE" and hasattr(self, 'caminho_em_construcao') and self.caminho_em_construcao:
                
                # Coleta todos os pontos X, Y da linha em uma lista de dicionários
                pontos = [{"x": p.x(), "y": p.y()} for p in self.caminho_em_construcao.pontos]
                
                if pontos: # Só envia se realmente desenhou algo
                    dados = {
                        "tipo": "Linha",
                        "posx": pontos[0]["x"], # X inicial
                        "posy": pontos[0]["y"], # Y inicial
                        "largura": 0,
                        "altura": 0,
                        "cor": self.obter_codigo_cor(self.cor_atual),
                        "texto": json.dumps(pontos) # Empacota os pontos como String (JSON)
                    }
                    print(f"[DEBUG - ENVIANDO] {dados}")
                    self.elemento_criado.emit(dados)
                
                # Limpa a variável para o próximo desenho local
                self.caminho_em_construcao = None

    #NOTE: Impede colocar forma sobre forma, evitar problemas no banco
    def espaco_livre(self, nova_caixa: QRectF) -> bool:
        for elemento in self.elementos:
            if elemento.caixa_contorno().intersects(nova_caixa):
                return False
        return True

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return

        pos_atual = event.position().toPoint()
        
        if self.elemento_selecionado and self.ferramenta_ativa == "MAO":
            dx = pos_atual.x() - self.ultimo_ponto_mouse.x()
            dy = pos_atual.y() - self.ultimo_ponto_mouse.y()
            
            if isinstance(self.elemento_selecionado, Linha):
                self.elemento_selecionado.mover(dx, dy)
            else:
                self.elemento_selecionado.x += dx
                self.elemento_selecionado.y += dy
                
            self.ultimo_ponto_mouse = pos_atual
            
        elif self.ferramenta_ativa == "LIVRE" and hasattr(self, 'caminho_em_construcao') and self.caminho_em_construcao:
            self.caminho_em_construcao.pontos.append(pos_atual)
            
        self.update()
        
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.drawImage(0, 0, self.image)
        
        for elemento in self.elementos:
            elemento.desenhar(painter)

    def resizeEvent(self, event):
        if self.image.size() != self.size():
            nova_imagem = QImage(self.size(), QImage.Format.Format_RGB32)
            nova_imagem.fill(Qt.GlobalColor.white)
            
            painter = QPainter(nova_imagem)
            painter.drawImage(QPoint(0, 0), self.image)
            painter.end()
            
            self.image = nova_imagem
        super().resizeEvent(event)

    def configurar_toolbar(self):
        toolbar = self.addToolBar("Ferramentas")
        
        toolbar.addAction("Limpar", self.limpar_quadro)
        
        # exibir nome da sala
        self.label_sala = QLabel("Sala: -")
        self.label_sala.setStyleSheet("font-weight: bold; font-size: 12px; color: #2c3e50; margin-left: 10px; margin-right: 15px;")
        toolbar.addWidget(self.label_sala)
        
        btn_componentes = QPushButton("Componentes")
        menu_principal = QMenu(self)
        
        opcoes = [("Mão (Seletor)", "MAO"),
                  ("Texto", "TEXTO"),
                  ("Quadrilátero", "QUADRILATERO"),
                  ("Círculo", "CIRCULO"),
                  ("Desenho Livre", "LIVRE")
                  ]
        for nome, tipo in opcoes:
            acao = menu_principal.addAction(nome)
            acao.triggered.connect(lambda chk, t=tipo: self.preparar_ferramenta(t))
            
        menu_seta = menu_principal.addMenu("Setas")
        direcoes = [
            ("Direita", "DIR"), ("Esquerda", "ESQ"),
            ("Baixo", "BAIXO"), ("Cima", "CIMA"),
            ("Diagonal Inf-Dir", "D_ID"), ("Diagonal Sup-Esq", "D_SE"),
            ("Diagonal Inf-Esq", "D_IE"), ("Diagonal Sup-Dir", "D_SD")
        ]
        for nome, sigla in direcoes:
            acao = menu_seta.addAction(nome)
            acao.triggered.connect(lambda chk, s=sigla: self.preparar_seta(s))
            
        btn_componentes.setMenu(menu_principal)
        toolbar.addWidget(btn_componentes)

    def preparar_ferramenta(self, tipo):
        self.ferramenta_ativa = tipo
        
        if tipo in ["QUADRILATERO", "CIRCULO"]:
            w, ok1 = QInputDialog.getInt(self, "Largura", "Valor:", 100, 1)
            h, ok2 = QInputDialog.getInt(self, "Altura", "Valor:", 100, 1)
            if ok1 and ok2:
                self.dimensoes = {"w": w, "h": h}
            else:
                self.ferramenta_ativa = "MAO" #NOTE: Cancela se o usuário fechar a janela
                
        elif tipo == "TEXTO":
            texto, ok1 = QInputDialog.getText(self, "Inserir Texto", "Digite o texto:")
            if ok1 and texto:
                tamanho, ok2 = QInputDialog.getInt(self, "Tamanho da Fonte", "Valor:", 24, 8, 150)
                if ok2:
                    self.texto_atual = texto
                    self.tamanho_fonte_atual = tamanho
                    self.dimensoes = {'w':100,'h':100}
                else:
                    self.ferramenta_ativa = "MAO"
            else:
                self.ferramenta_ativa = "MAO"

        self.elemento_selecionado = None
        self.statusBar().showMessage(f"Modo: {self.ferramenta_ativa}")
        self.update()

    def preparar_seta(self, direcao):
        self.ferramenta_ativa = "SETA"
        self.direcao_seta_atual = direcao
        
        tamanho, ok = QInputDialog.getInt(self, "Tamanho da Seta", "Comprimento (px):", 80, 10, 500)
        
        if ok:
            self.tamanho_seta_atual = tamanho
        else:
            self.tamanho_seta_atual = 80 #NOTE: Default caso cancele
            
        self.statusBar().showMessage(f"Seta {direcao} preparada. Clique para inserir.")

    def definir_sala(self, id_sala):
        self.id_sala = id_sala
        self.label_sala.setText(f"Sala: {id_sala}")

    def obter_codigo_cor(self, qcolor):
        if qcolor == QColor(Qt.GlobalColor.black): return 0
        if qcolor == QColor(Qt.GlobalColor.red): return 1
        if qcolor == QColor(Qt.GlobalColor.blue): return 2
        if qcolor == QColor(Qt.GlobalColor.green): return 3
        return 0

    def mapear_tipo(self, ferramenta):
        mapa = {
            "QUADRILATERO": "Retangulo",
            "CIRCULO": "Circulo",
            "SETA": "Seta",
            "TEXTO": "Texto",
            "LIVRE": "Linha"
        }
        return mapa.get(ferramenta, "Retangulo")


    def adicionar_elemento_rede(self, dados):
        tipo = dados.get("tipo")
        
        mapa_cores = {
            0: QColor(Qt.GlobalColor.black), 1: QColor(Qt.GlobalColor.red),
            2: QColor(Qt.GlobalColor.blue), 3: QColor(Qt.GlobalColor.green),
        }
        cor = mapa_cores.get(dados.get("cor", 0), QColor(Qt.GlobalColor.black))

        px, py = dados.get("posx", 0), dados.get("posy", 0)
        w, h = dados.get("largura", 100), dados.get("altura", 100)
        texto = dados.get("texto", "")

        if tipo == "Retangulo":
            novo = Retangulo(px, py, w, h, cor)
            self.elementos.append(novo)
        elif tipo == "Circulo":
            novo = Circulo(px, py, w, h, cor)
            self.elementos.append(novo)
        elif tipo == "Seta":
            dir_seta = texto if texto else "DIR"
            novo = Seta(px, py, cor, dir_seta, w)
            self.elementos.append(novo)

        elif tipo == "Texto":
            try:
                print(f"DEBUG RECEBIDO -> Texto: {texto}, X: {px}, Y: {py}, Cor: {cor}")
                # O tamanho da fonte foi enviado embutido na variável 'h' (altura)
                tamanho_fonte = int(h) if int(h) > 0 else 24
                
                # Garante que seja lido como string
                frase = str(texto) if texto else "Texto"
                
                # Usamos exatamente as mesmas dimensões padrão da criação local (100x100)
                # para evitar que a caixa de contorno quebre a renderização do componente
                novo = Texto(int(px), int(py), 400, 400, frase, tamanho_fonte, cor)
                
                self.elementos.append(novo)
                
            except Exception as e:
                print(f"Erro ao renderizar Texto da rede: {e}")

        elif tipo == "Linha":
            try:
                pontos = json.loads(texto) if texto else []
                novo = Linha(cor)
                for p in pontos:
                    novo.pontos.append(QPoint(p["x"], p["y"]))
                self.elementos.append(novo)
            except Exception as e:
                print(f"Erro ao renderizar linha da rede: {e}")
            
        print(f"DEBUG RECEBIDO -> Texto: {texto}, X: {px}, Y: {py}, Cor: {cor}")
        self.update()
