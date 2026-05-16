import sqlite3
from typing import TypedDict, Literal, NotRequired
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
