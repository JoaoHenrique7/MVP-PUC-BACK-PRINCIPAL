import sqlite3

DB_NAME = "enderecos.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enderecos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cep TEXT NOT NULL,
            logradouro TEXT,
            bairro TEXT,
            localidade TEXT,
            uf TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_endereco(cep: str, logradouro: str, bairro: str, localidade: str, uf: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO enderecos (cep, logradouro, bairro, localidade, uf)
        VALUES (?, ?, ?, ?, ?)
    """, (cep, logradouro, bairro, localidade, uf))
    conn.commit()
    conn.close()

def get_enderecos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enderecos")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "cep": row[1],
            "logradouro": row[2],
            "bairro": row[3],
            "localidade": row[4],
            "uf": row[5],
        }
        for row in rows
    ]

def update_endereco(endereco_id: int, logradouro: str, bairro: str, localidade: str, uf: str) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE enderecos
        SET logradouro=?, bairro=?, localidade=?, uf=?
        WHERE id=?
    """, (logradouro, bairro, localidade, uf, endereco_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated

def delete_endereco(endereco_id: int) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enderecos WHERE id=?", (endereco_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted
