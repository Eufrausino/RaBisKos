import sqlite3
import os
import logging

DB_PATH = os.environ.get('DB_PATH', os.path.join(os.path.dirname(__file__), 'sistema.db'))
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'script-sql', 'schema.sql')

def obter_conexao():
    return sqlite3.connect(DB_PATH)

def inicializar_banco():
    if not os.path.exists(SCHEMA_PATH):
        logging.debug(f"[ERRO] Arquivo de esquema não encontrado em: {SCHEMA_PATH}")
        return

    try:
        with open(SCHEMA_PATH, 'r') as f:
            script_sql = f.read()

        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        # executescript permite rodar múltiplas instruções separadas por ;
        cursor.executescript(script_sql)
        
        conexao.commit()
        conexao.close()
        logging.debug("[SUCESSO] Estrutura do banco de dados verificada/atualizada.")
    except Exception as e:
        logging.debug(f"[ERRO] Falha ao inicializar banco: {e}")
