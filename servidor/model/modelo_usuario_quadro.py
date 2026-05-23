import sqlite3
from .banco_de_dados.modelo_banco import obter_conexao

class UsuarioQuadroModelo:
    @staticmethod
    def inserir(idUsuario: int, idQuadro: int): ## toda vez que logar 
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            
            # prevenir que o mesmo usuário seja adicionado várias vezes ao mesmo quadro
            cursor.execute('SELECT 1 FROM usuarioQuadro WHERE IdUsuario = ? AND IdQuadro = ?', (idUsuario, idQuadro))
            if cursor.fetchone():
                conexao.close()
                return False, "O usuário já possui acesso a este quadro"
                
            cursor.execute('INSERT INTO usuarioQuadro (IdUsuario, IdQuadro) VALUES (?, ?)', (idUsuario, idQuadro))
            conexao.commit()
            conexao.close()
            return True, "Usuário vinculado ao quadro com sucesso"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def remover(idUsuario: int, idQuadro: int): ## pode ser util
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            
            cursor.execute('DELETE FROM usuarioQuadro WHERE IdUsuario = ? AND IdQuadro = ?', (idUsuario, idQuadro))
            conexao.commit()
            linhas_afetadas = cursor.rowcount
            conexao.close()
            
            if linhas_afetadas > 0:
                return True, "Acesso do usuário ao quadro foi removido"
            else:
                return False, "Vínculo entre o usuário e o quadro não foi encontrado"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def buscar_quadros_por_usuario(idUsuario: int): ## util se tiver historico
        try:
            conexao = obter_conexao()
            conexao.row_factory = sqlite3.Row
            cursor = conexao.cursor()
            cursor.execute('''
                SELECT q.* 
                FROM usuarioQuadro uq
                JOIN quadros q ON uq.IdQuadro = q.IdQuadro
                WHERE uq.IdUsuario = ?
            ''', (idUsuario,))

            resultado = [dict(row) for row in cursor.fetchall()]
            conexao.close()
            return True, resultado
        except Exception as e:
            return False, str(e)


