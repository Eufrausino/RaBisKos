import sqlite3
import random
import string
from .banco_de_dados.modelo_banco import obter_conexao

class QuadroModelo:
    @staticmethod
    def inserir(idUsuarioDono: int):
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            
            # Tenta gerar um ID único (5 caracteres maiúsculos + números)
            for _ in range(5):
                idQuadroSala = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                try:
                    cursor.execute('INSERT INTO quadros (IdUsuarioDono, IdQuadroSala) VALUES (?, ?)', (idUsuarioDono, idQuadroSala))
                    conexao.commit()
                    conexao.close()
                    
                    return True, idQuadroSala
                except sqlite3.IntegrityError:
                    continue
            
            conexao.close()
            return False, "Falha ao gerar um identificador único para a sala"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def buscar_quadro_por_idQuadroSala(idQuadroSala: str):
        try:
            conexao = obter_conexao()
            
            conexao.row_factory = sqlite3.Row
            cursor = conexao.cursor()
            
            cursor.execute('SELECT * FROM quadros WHERE IdQuadroSala = ?', (idQuadroSala,))
            resultado = cursor.fetchone()
            conexao.close()
            
            if resultado:
                return True, dict(resultado)
            else:
                return False, "Sala não encontrada"
        except Exception as e:
            return False, str(e)