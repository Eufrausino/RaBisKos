import sqlite3
#Mudei aqui, Eduardo
#from typing import TypedDict, Literal, NotRequired
from typing import TypedDict, Literal

try:
    from typing import NotRequired
except ImportError:
    from typing_extensions import NotRequired
    
from .banco_de_dados.modelo_banco import obter_conexao

class ElementoDados(TypedDict):
    tipo: NotRequired[Literal['Retangulo', 'Quadrado', 'Circulo', 'Triangulo', 'Linha', 'Seta']]
    posx: int
    posy: int
    largura: int
    altura: int
    cor: int  # 0: Preto, 1: Branco, 2: Vermelho, 3: Verde, 4: Azul, 5: Amarelo
    texto: NotRequired[str]  

class ElementoModelo:
    @staticmethod
    def inserir(idQuadro: int, dados: ElementoDados, versao: int):
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            
            cursor.execute(
                '''
                INSERT INTO elementos (IdQuadro, Tipo, PosX, PosY, Largura, Altura, Cor, Texto, Versao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    idQuadro,
                    dados.get('tipo'),
                    dados['posx'],
                    dados['posy'],
                    dados['largura'],
                    dados['altura'],
                    dados['cor'],
                    dados.get('texto'),
                    versao
                )
            )
            conexao.commit()
            conexao.close()
            return True, "Elemento inserido com sucesso"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def atualizar(idElemento: int, dados: ElementoDados, versao: int):
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            
            cursor.execute(
                '''
                UPDATE elementos 
                SET Tipo = ?, PosX = ?, PosY = ?, Largura = ?, Altura = ?, Cor = ?, Texto = ?, Versao = ?
                WHERE IdElemento = ?
                ''',
                (
                    dados.get('tipo'),
                    dados['posx'],
                    dados['posy'],
                    dados['largura'],
                    dados['altura'],
                    dados['cor'],
                    dados.get('texto'),
                    versao,
                    idElemento
                )
            )
            conexao.commit()
            linhas_afetadas = cursor.rowcount
            conexao.close()
            
            if linhas_afetadas > 0:
                return True, "Elemento atualizado com sucesso"
            else:
                return False, "Elemento não encontrado"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def remover(idElemento: int):
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            
            cursor.execute('DELETE FROM elementos WHERE IdElemento = ?', (idElemento,))
            conexao.commit()
            linhas_afetadas = cursor.rowcount
            conexao.close()
            
            if linhas_afetadas > 0:
                return True, "Elemento removido com sucesso"
            else:
                return False, "Elemento não encontrado"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def listar_por_quadro(idQuadro: int):
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            
            cursor.execute('SELECT IdElemento, Tipo, PosX, PosY, Largura, Altura, Cor, Texto, Versao FROM elementos WHERE IdQuadro = ?', (idQuadro,))
            linhas = cursor.fetchall()
            conexao.close()
            
            elementos = []
            for linha in linhas:
                elementos.append({
                    "idElemento": linha[0],
                    "tipo": linha[1],
                    "posx": linha[2],
                    "posy": linha[3],
                    "largura": linha[4],
                    "altura": linha[5],
                    "cor": linha[6],
                    "texto": linha[7] or "",
                    "versao": linha[8]
                })
            return True, elementos
        except Exception as e:
            return False, str(e)
