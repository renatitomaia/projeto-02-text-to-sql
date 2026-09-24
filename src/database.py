import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join("database", "db_obra.db")

def get_connection():
    """Retorna a conexão com o banco SQLite."""
    return sqlite3.connect(DB_PATH)

def get_db_schema():
    """
    Retorna a estrutura DDL de todas as tabelas no banco de dados.
    Isso é enviado ao prompt da IA para que ela conheça as tabelas e colunas.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    
    schema_str = "\n\n".join([table[0] for table in tables if table[0] is not None])
    return schema_str

def execute_query(query: str):
    """
    Executa a query SQL no banco de dados e retorna o resultado em DataFrame.
    """
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        conn.close()
        return None, str(e)