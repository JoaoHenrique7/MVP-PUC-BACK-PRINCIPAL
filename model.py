import sqlite3

def init_db():
    conn = sqlite3.connect("enderecos.db")
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

def get_enderecos_paginados(pagina=1, por_pagina=10):
    offset = (pagina - 1) * por_pagina
    
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    
    # Obtém os endereços da página atual
    cursor.execute("SELECT * FROM enderecos LIMIT ? OFFSET ?", (por_pagina, offset))
    enderecos = cursor.fetchall()
    
    # Conta o total de endereços
    cursor.execute("SELECT COUNT(*) FROM enderecos")
    total_enderecos = cursor.fetchone()[0]
    
    conn.close()
    
    # Calcula informações de paginação
    total_paginas = (total_enderecos + por_pagina - 1) // por_pagina
    tem_proxima = pagina < total_paginas
    tem_anterior = pagina > 1
    
    # Converte para dicionários
    enderecos_dict = []
    for endereco in enderecos:
        enderecos_dict.append({
            "id": endereco[0],
            "cep": endereco[1],
            "logradouro": endereco[2],
            "bairro": endereco[3],
            "localidade": endereco[4],
            "uf": endereco[5]
        })
    
    return {
        "enderecos": enderecos_dict,
        "pagina_atual": pagina,
        "por_pagina": por_pagina,
        "total_enderecos": total_enderecos,
        "total_paginas": total_paginas,
        "tem_proxima": tem_proxima,
        "tem_anterior": tem_anterior
    }

# Mantenha as outras funções existentes (get_enderecos, insert_endereco, update_endereco, delete_endereco)
def get_enderecos():
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enderecos")
    enderecos = cursor.fetchall()
    conn.close()
    
    enderecos_dict = []
    for endereco in enderecos:
        enderecos_dict.append({
            "id": endereco[0],
            "cep": endereco[1],
            "logradouro": endereco[2],
            "bairro": endereco[3],
            "localidade": endereco[4],
            "uf": endereco[5]
        })
    
    return enderecos_dict

def insert_endereco(cep, logradouro, bairro, localidade, uf):
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO enderecos (cep, logradouro, bairro, localidade, uf)
        VALUES (?, ?, ?, ?, ?)
    """, (cep, logradouro, bairro, localidade, uf))
    conn.commit()
    conn.close()

def update_endereco(endereco_id, logradouro, bairro, localidade, uf):
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE enderecos 
        SET logradouro=?, bairro=?, localidade=?, uf=?
        WHERE id=?
    """, (logradouro, bairro, localidade, uf, endereco_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected

def delete_endereco(endereco_id):
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enderecos WHERE id=?", (endereco_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected