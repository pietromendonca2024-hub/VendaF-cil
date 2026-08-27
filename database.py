import sqlite3
import hashlib
import secrets
import hmac

from datetime import (
    datetime,
    timedelta
)

import sqlite3
import hashlib
import secrets
import hmac
import shutil

from datetime import (
    datetime,
    timedelta
)

from pathlib import Path

from app_paths import caminho_banco


BANCO = caminho_banco()


def migrar_banco_antigo():
    """
    Copia automaticamente o database.db antigo da pasta
    do projeto para o AppData na primeira execução.
    """

    destino = Path(
        BANCO
    )

    if destino.exists():
        return

    banco_antigo = (
        Path(__file__)
        .resolve()
        .parent
        / "database.db"
    )

    if banco_antigo.exists():
        destino.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            banco_antigo,
            destino
        )
        
ITERACOES_SENHA = 200_000

MAX_TENTATIVAS_LOGIN = 5

TEMPO_BLOQUEIO_MINUTOS = 5


# =========================================================
# CONEXÃO
# =========================================================

def conectar():
    conn = sqlite3.connect(
        BANCO,
        timeout=10
    )

    conn.row_factory = sqlite3.Row

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    conn.execute(
        "PRAGMA journal_mode = WAL"
    )

    conn.execute(
        "PRAGMA synchronous = NORMAL"
    )

    return conn


# =========================================================
# MIGRAÇÕES
# =========================================================

def coluna_existe(
    conn,
    tabela,
    coluna
):
    colunas = conn.execute(
        f"PRAGMA table_info({tabela})"
    ).fetchall()

    return any(
        item["name"] == coluna
        for item in colunas
    )


def atualizar_estrutura_usuarios(
    conn
):
    if not coluna_existe(
        conn,
        "usuarios",
        "tentativas_falhas"
    ):
        conn.execute("""
            ALTER TABLE usuarios
            ADD COLUMN tentativas_falhas
            INTEGER NOT NULL DEFAULT 0
        """)

    if not coluna_existe(
        conn,
        "usuarios",
        "bloqueado_ate"
    ):
        conn.execute("""
            ALTER TABLE usuarios
            ADD COLUMN bloqueado_ate TEXT
        """)

    if not coluna_existe(
        conn,
        "usuarios",
        "ultimo_login"
    ):
        conn.execute("""
            ALTER TABLE usuarios
            ADD COLUMN ultimo_login TEXT
        """)

    if not coluna_existe(
        conn,
        "usuarios",
        "senha_alterada_em"
    ):
        conn.execute("""
            ALTER TABLE usuarios
            ADD COLUMN senha_alterada_em TEXT
        """)


# =========================================================
# CRIAR BANCO
# =========================================================

def criar_banco():
    conn = conectar()

    cursor = conn.cursor()

    # =====================
    # PRODUTOS
    # =====================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            preco REAL NOT NULL,

            ativo INTEGER NOT NULL DEFAULT 1,

            criado_em TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # =====================
    # VENDAS
    # =====================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            total REAL NOT NULL,

            forma_pagamento TEXT NOT NULL,

            data TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # =====================
    # ITENS
    # =====================

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

    # =====================
    # USUÁRIOS
    # =====================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario TEXT NOT NULL UNIQUE,

            senha_hash TEXT NOT NULL,

            salt TEXT NOT NULL,

            ativo INTEGER NOT NULL DEFAULT 1,

            tentativas_falhas
            INTEGER NOT NULL DEFAULT 0,

            bloqueado_ate TEXT,

            ultimo_login TEXT,

            senha_alterada_em TEXT,

            criado_em TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        )
    """)

    atualizar_estrutura_usuarios(
        conn
    )

    conn.commit()

    conn.close()


# =========================================================
# SEGURANÇA DE SENHA
# =========================================================

def validar_senha(
    senha
):
    if len(senha) < 8:
        raise ValueError(
            "A senha deve possuir "
            "pelo menos 8 caracteres."
        )

    if not any(
        caractere.isalpha()
        for caractere in senha
    ):
        raise ValueError(
            "A senha deve possuir "
            "pelo menos uma letra."
        )

    if not any(
        caractere.isdigit()
        for caractere in senha
    ):
        raise ValueError(
            "A senha deve possuir "
            "pelo menos um número."
        )


def gerar_hash_senha(
    senha,
    salt=None
):
    if salt is None:
        salt_bytes = secrets.token_bytes(
            32
        )

    else:
        salt_bytes = bytes.fromhex(
            salt
        )

    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode(
            "utf-8"
        ),
        salt_bytes,
        ITERACOES_SENHA
    )

    return (
        hash_bytes.hex(),
        salt_bytes.hex()
    )


# =========================================================
# USUÁRIOS
# =========================================================

def existe_usuario():
    conn = conectar()

    resultado = conn.execute("""
        SELECT COUNT(*)

        FROM usuarios

        WHERE ativo = 1
    """).fetchone()[0]

    conn.close()

    return resultado > 0


def cadastrar_usuario(
    usuario,
    senha
):
    usuario = usuario.strip()

    if not usuario:
        raise ValueError(
            "Informe um usuário."
        )

    if len(usuario) < 3:
        raise ValueError(
            "O usuário deve possuir "
            "pelo menos 3 caracteres."
        )

    validar_senha(
        senha
    )

    senha_hash, salt = gerar_hash_senha(
        senha
    )

    agora = datetime.now().isoformat(
        timespec="seconds"
    )

    conn = conectar()

    try:
        conn.execute("""
            INSERT INTO usuarios (
                usuario,
                senha_hash,
                salt,
                senha_alterada_em
            )

            VALUES (?, ?, ?, ?)
        """, (
            usuario,
            senha_hash,
            salt,
            agora
        ))

        conn.commit()

    except sqlite3.IntegrityError:

        raise ValueError(
            "Este nome de usuário "
            "já está cadastrado."
        )

    finally:
        conn.close()


# =========================================================
# LOGIN
# =========================================================

def autenticar_usuario(
    usuario,
    senha
):
    usuario = usuario.strip()

    conn = conectar()

    registro = conn.execute("""
        SELECT *

        FROM usuarios

        WHERE usuario = ?
        AND ativo = 1

        LIMIT 1
    """, (
        usuario,
    )).fetchone()

    # Faz um cálculo mesmo quando o usuário
    # não existe para reduzir diferença de tempo.
    if not registro:
        dummy_salt = (
            "00" * 32
        )

        gerar_hash_senha(
            senha,
            dummy_salt
        )

        conn.close()

        return {
            "sucesso": False,
            "motivo": "credenciais"
        }

    agora = datetime.now()

    bloqueado_ate = registro[
        "bloqueado_ate"
    ]

    # =====================
    # VERIFICAR BLOQUEIO
    # =====================

    if bloqueado_ate:
        try:
            fim_bloqueio = (
                datetime.fromisoformat(
                    bloqueado_ate
                )
            )

        except ValueError:
            fim_bloqueio = None

        if (
            fim_bloqueio
            and agora < fim_bloqueio
        ):
            segundos = int(
                (
                    fim_bloqueio
                    - agora
                ).total_seconds()
            )

            conn.close()

            return {
                "sucesso": False,
                "motivo": "bloqueado",
                "segundos": segundos
            }

        # Bloqueio expirou.
        conn.execute("""
            UPDATE usuarios

            SET
                tentativas_falhas = 0,
                bloqueado_ate = NULL

            WHERE id = ?
        """, (
            registro["id"],
        ))

        conn.commit()

        tentativas_atuais = 0

    else:
        tentativas_atuais = (
            registro["tentativas_falhas"]
            or 0
        )

    # =====================
    # VERIFICAR SENHA
    # =====================

    hash_digitado, _ = gerar_hash_senha(
        senha,
        registro["salt"]
    )

    senha_valida = hmac.compare_digest(
        hash_digitado,
        registro["senha_hash"]
    )

    # =====================
    # SENHA ERRADA
    # =====================

    if not senha_valida:
        novas_tentativas = (
            tentativas_atuais + 1
        )

        if novas_tentativas >= (
            MAX_TENTATIVAS_LOGIN
        ):
            fim_bloqueio = (
                agora
                + timedelta(
                    minutes=
                    TEMPO_BLOQUEIO_MINUTOS
                )
            )

            conn.execute("""
                UPDATE usuarios

                SET
                    tentativas_falhas = ?,
                    bloqueado_ate = ?

                WHERE id = ?
            """, (
                novas_tentativas,
                fim_bloqueio.isoformat(
                    timespec="seconds"
                ),
                registro["id"]
            ))

            conn.commit()

            conn.close()

            return {
                "sucesso": False,
                "motivo": "bloqueado",
                "segundos":
                    TEMPO_BLOQUEIO_MINUTOS
                    * 60
            }

        conn.execute("""
            UPDATE usuarios

            SET tentativas_falhas = ?

            WHERE id = ?
        """, (
            novas_tentativas,
            registro["id"]
        ))

        conn.commit()

        restantes = (
            MAX_TENTATIVAS_LOGIN
            - novas_tentativas
        )

        conn.close()

        return {
            "sucesso": False,
            "motivo": "credenciais",
            "tentativas_restantes":
                restantes
        }

    # =====================
    # LOGIN CORRETO
    # =====================

    conn.execute("""
        UPDATE usuarios

        SET
            tentativas_falhas = 0,
            bloqueado_ate = NULL,
            ultimo_login = ?

        WHERE id = ?
    """, (
        agora.isoformat(
            timespec="seconds"
        ),
        registro["id"]
    ))

    conn.commit()

    conn.close()

    return {
        "sucesso": True,

        "usuario": {
            "id":
                registro["id"],

            "usuario":
                registro["usuario"]
        }
    }


# =========================================================
# ALTERAR SENHA
# =========================================================

def alterar_senha(
    usuario_id,
    senha_atual,
    nova_senha
):
    validar_senha(
        nova_senha
    )

    if senha_atual == nova_senha:
        raise ValueError(
            "A nova senha deve ser "
            "diferente da senha atual."
        )

    conn = conectar()

    registro = conn.execute("""
        SELECT *

        FROM usuarios

        WHERE id = ?
        AND ativo = 1

        LIMIT 1
    """, (
        usuario_id,
    )).fetchone()

    if not registro:
        conn.close()

        raise ValueError(
            "Usuário não encontrado."
        )

    hash_atual, _ = gerar_hash_senha(
        senha_atual,
        registro["salt"]
    )

    if not hmac.compare_digest(
        hash_atual,
        registro["senha_hash"]
    ):
        conn.close()

        raise ValueError(
            "A senha atual está incorreta."
        )

    novo_hash, novo_salt = (
        gerar_hash_senha(
            nova_senha
        )
    )

    agora = datetime.now().isoformat(
        timespec="seconds"
    )

    conn.execute("""
        UPDATE usuarios

        SET
            senha_hash = ?,
            salt = ?,
            senha_alterada_em = ?,
            tentativas_falhas = 0,
            bloqueado_ate = NULL

        WHERE id = ?
    """, (
        novo_hash,
        novo_salt,
        agora,
        usuario_id
    ))

    conn.commit()

    conn.close()


# =========================================================
# PRODUTOS
# =========================================================

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


def cadastrar_produto(
    nome,
    preco
):
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


def atualizar_produto(
    produto_id,
    nome,
    preco
):
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


def excluir_produto(
    produto_id
):
    conn = conectar()

    conn.execute("""
        UPDATE produtos

        SET ativo = 0

        WHERE id = ?
    """, (
        produto_id,
    ))

    conn.commit()

    conn.close()


# =========================================================
# VENDAS
# =========================================================

def registrar_venda(
    itens,
    forma_pagamento
):
    if not itens:
        return None

    conn = conectar()

    cursor = conn.cursor()

    try:
        total = sum(
            item["preco"]
            * item["quantidade"]

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

        venda_id = (
            cursor.lastrowid
        )

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


# =========================================================
# HISTÓRICO
# =========================================================

def listar_vendas():
    conn = conectar()

    vendas = conn.execute("""
        SELECT
            id,
            total,
            forma_pagamento,
            data

        FROM vendas

        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return vendas


def listar_itens_venda(
    venda_id
):
    conn = conectar()

    itens = conn.execute("""
        SELECT
            produtos.nome,

            venda_itens.quantidade,

            venda_itens.preco_unitario,

            venda_itens.subtotal

        FROM venda_itens

        JOIN produtos
        ON produtos.id =
        venda_itens.produto_id

        WHERE venda_itens.venda_id = ?

        ORDER BY venda_itens.id
    """, (
        venda_id,
    )).fetchall()

    conn.close()

    return itens


# =========================================================
# DASHBOARD
# =========================================================

def dados_dashboard():
    conn = conectar()

    faturamento_hoje = conn.execute("""
        SELECT COALESCE(
            SUM(total),
            0
        )

        FROM vendas

        WHERE DATE(data)
        = DATE('now', 'localtime')
    """).fetchone()[0]

    vendas_hoje = conn.execute("""
        SELECT COUNT(*)

        FROM vendas

        WHERE DATE(data)
        = DATE('now', 'localtime')
    """).fetchone()[0]

    total_produtos = conn.execute("""
        SELECT COUNT(*)

        FROM produtos

        WHERE ativo = 1
    """).fetchone()[0]

    itens_hoje = conn.execute("""
        SELECT COALESCE(
            SUM(
                venda_itens.quantidade
            ),
            0
        )

        FROM venda_itens

        JOIN vendas
        ON vendas.id =
        venda_itens.venda_id

        WHERE DATE(vendas.data)
        = DATE('now', 'localtime')
    """).fetchone()[0]

    if vendas_hoje > 0:
        ticket_medio = (
            faturamento_hoje
            / vendas_hoje
        )

    else:
        ticket_medio = 0

    pagamentos = conn.execute("""
        SELECT
            forma_pagamento,

            COUNT(*) AS quantidade,

            COALESCE(
                SUM(total),
                0
            ) AS total

        FROM vendas

        WHERE DATE(data)
        = DATE('now', 'localtime')

        GROUP BY forma_pagamento

        ORDER BY total DESC
    """).fetchall()

    ultimas_vendas = conn.execute("""
        SELECT
            id,
            total,
            forma_pagamento,
            data

        FROM vendas

        ORDER BY id DESC

        LIMIT 5
    """).fetchall()

    produto_mais_vendido = conn.execute("""
        SELECT
            produtos.nome,

            SUM(
                venda_itens.quantidade
            ) AS quantidade

        FROM venda_itens

        JOIN produtos
        ON produtos.id =
        venda_itens.produto_id

        JOIN vendas
        ON vendas.id =
        venda_itens.venda_id

        WHERE DATE(vendas.data)
        = DATE('now', 'localtime')

        GROUP BY
            produtos.id,
            produtos.nome

        ORDER BY quantidade DESC

        LIMIT 1
    """).fetchone()

    conn.close()

    return {
        "faturamento_hoje":
            faturamento_hoje,

        "vendas_hoje":
            vendas_hoje,

        "total_produtos":
            total_produtos,

        "itens_hoje":
            itens_hoje,

        "ticket_medio":
            ticket_medio,

        "pagamentos":
            pagamentos,

        "ultimas_vendas":
            ultimas_vendas,

        "produto_mais_vendido":
            produto_mais_vendido
    }


# =========================================================
# RELATÓRIO MENSAL
# =========================================================

def dados_relatorio_mensal(
    ano,
    mes
):
    conn = conectar()

    ano = str(
        ano
    )

    mes = f"{int(mes):02d}"

    resumo = conn.execute("""
        SELECT
            COUNT(*) AS vendas,

            COALESCE(
                SUM(total),
                0
            ) AS faturamento,

            COALESCE(
                AVG(total),
                0
            ) AS ticket_medio

        FROM vendas

        WHERE strftime(
            '%Y',
            data
        ) = ?

        AND strftime(
            '%m',
            data
        ) = ?
    """, (
        ano,
        mes
    )).fetchone()

    itens_vendidos = conn.execute("""
        SELECT COALESCE(
            SUM(
                venda_itens.quantidade
            ),
            0
        )

        FROM venda_itens

        JOIN vendas
        ON vendas.id =
        venda_itens.venda_id

        WHERE strftime(
            '%Y',
            vendas.data
        ) = ?

        AND strftime(
            '%m',
            vendas.data
        ) = ?
    """, (
        ano,
        mes
    )).fetchone()[0]

    pagamentos = conn.execute("""
        SELECT
            forma_pagamento,

            COUNT(*) AS quantidade_vendas,

            COALESCE(
                SUM(total),
                0
            ) AS total

        FROM vendas

        WHERE strftime(
            '%Y',
            data
        ) = ?

        AND strftime(
            '%m',
            data
        ) = ?

        GROUP BY forma_pagamento

        ORDER BY total DESC
    """, (
        ano,
        mes
    )).fetchall()

    produtos = conn.execute("""
        SELECT
            produtos.nome,

            SUM(
                venda_itens.quantidade
            ) AS quantidade,

            SUM(
                venda_itens.subtotal
            ) AS faturamento

        FROM venda_itens

        JOIN vendas
        ON vendas.id =
        venda_itens.venda_id

        JOIN produtos
        ON produtos.id =
        venda_itens.produto_id

        WHERE strftime(
            '%Y',
            vendas.data
        ) = ?

        AND strftime(
            '%m',
            vendas.data
        ) = ?

        GROUP BY
            produtos.id,
            produtos.nome

        ORDER BY quantidade DESC
    """, (
        ano,
        mes
    )).fetchall()

    vendas_por_dia = conn.execute("""
        SELECT
            DATE(data) AS dia,

            COUNT(*) AS quantidade,

            COALESCE(
                SUM(total),
                0
            ) AS total

        FROM vendas

        WHERE strftime(
            '%Y',
            data
        ) = ?

        AND strftime(
            '%m',
            data
        ) = ?

        GROUP BY DATE(data)

        ORDER BY DATE(data)
    """, (
        ano,
        mes
    )).fetchall()

    conn.close()

    return {
        "vendas":
            resumo["vendas"],

        "faturamento":
            resumo["faturamento"],

        "ticket_medio":
            resumo["ticket_medio"],

        "itens_vendidos":
            itens_vendidos,

        "pagamentos":
            pagamentos,

        "produtos":
            produtos,

        "vendas_por_dia":
            vendas_por_dia
    }