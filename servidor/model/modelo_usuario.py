import sqlite3
from .bd_base import obter_conexao

class UsuarioModelo:
    """
    Data Access Object (DAO) para a tabela de usuários.
    Encapsula todas as operações SQL desta entidade.
    """
    
    @staticmethod
    def inserir(usuario, senha):
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute('INSERT INTO usuarios (usuario, senha) VALUES (?, ?)', (usuario, senha))
            conexao.commit()
            conexao.close()
            return True, "Usuário registrado com sucesso"
        except sqlite3.IntegrityError:
            return False, "Nome de usuário já existe"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def buscar_por_credenciais(usuario, senha):
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha))
            resultado = cursor.fetchone()
            conexao.close()
            return resultado
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None
