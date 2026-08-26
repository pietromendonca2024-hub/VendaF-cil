import sqlite3


BANCO = "database.db"


def conectar():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn


def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    # Produtos/comidas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Venda principal
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL NOT NULL,
            forma_pagamento TEXT NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Itens de cada venda
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venda_itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,

            FOREIGN KEY (venda_id)
                REFERENCES vendas(id),

            FOREIGN KEY (produto_id)
                REFERENCES produtos(id)
        )
    """)

    conn.commit()
    conn.close()


def dados_dashboard():
    conn = conectar()

    faturamento_hoje = conn.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM vendas
        WHERE DATE(data) = DATE('now', 'localtime')
    """).fetchone()[0]

    vendas_hoje = conn.execute("""
        SELECT COUNT(*)
        FROM vendas
        WHERE DATE(data) = DATE('now', 'localtime')
    """).fetchone()[0]

    total_produtos = conn.execute("""
        SELECT COUNT(*)
        FROM produtos
        WHERE ativo = 1
    """).fetchone()[0]

    itens_hoje = conn.execute("""
        SELECT COALESCE(SUM(venda_itens.quantidade), 0)
        FROM venda_itens

        JOIN vendas
        ON vendas.id = venda_itens.venda_id

        WHERE DATE(vendas.data)
            = DATE('now', 'localtime')
    """).fetchone()[0]

    conn.close()

    return {
        "faturamento_hoje": faturamento_hoje,
        "vendas_hoje": vendas_hoje,
        "total_produtos": total_produtos,
        "itens_hoje": itens_hoje
    }


def listar_produtos():
    conn = conectar()

    produtos = conn.execute("""
        SELECT *
        FROM produtos
        WHERE ativo = 1
        ORDER BY nome
    """).fetchall()

    conn.close()

    return produtos


def cadastrar_produto(nome, preco):
    conn = conectar()

    conn.execute("""
        INSERT INTO produtos (
            nome,
            preco
        )
        VALUES (?, ?)
    """, (
        nome,
        preco
    ))

    conn.commit()
    conn.close()


def atualizar_produto(produto_id, nome, preco):
    conn = conectar()

    conn.execute("""
        UPDATE produtos
        SET
            nome = ?,
            preco = ?
        WHERE id = ?
    """, (
        nome,
        preco,
        produto_id
    ))

    conn.commit()
    conn.close()


def excluir_produto(produto_id):
    conn = conectar()

    # Não apaga de verdade para preservar vendas antigas.
    conn.execute("""
        UPDATE produtos
        SET ativo = 0
        WHERE id = ?
    """, (
        produto_id,
    ))

    conn.commit()
    conn.close()


def registrar_venda(itens, forma_pagamento):
    if not itens:
        return None

    conn = conectar()
    cursor = conn.cursor()

    try:
        total = sum(
            item["preco"] * item["quantidade"]
            for item in itens
        )

        cursor.execute("""
            INSERT INTO vendas (
                total,
                forma_pagamento
            )
            VALUES (?, ?)
        """, (
            total,
            forma_pagamento
        ))

        venda_id = cursor.lastrowid

        for item in itens:
            subtotal = (
                item["preco"]
                * item["quantidade"]
            )

            cursor.execute("""
                INSERT INTO venda_itens (
                    venda_id,
                    produto_id,
                    quantidade,
                    preco_unitario,
                    subtotal
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                venda_id,
                item["id"],
                item["quantidade"],
                item["preco"],
                subtotal
            ))

        conn.commit()

        return venda_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()