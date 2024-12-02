# init_db.py
import sqlite3

db_path = 'dados.db'

def criar_banco_dados():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS planilha (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_arquivo TEXT NOT NULL,
        data_download TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        unidade TEXT NOT NULL,
        valor REAL NOT NULL,
        planilha_id INTEGER,
        FOREIGN KEY (planilha_id) REFERENCES planilha (id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_banco_dados()
