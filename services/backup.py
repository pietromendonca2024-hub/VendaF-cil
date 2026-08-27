import sqlite3

from datetime import datetime

from app_paths import (
    caminho_banco,
    pasta_backups
)


BANCO = caminho_banco()

PASTA_BACKUPS = pasta_backups()

MAX_BACKUPS = 30


# =========================================================
# CRIAR BACKUP
# =========================================================

def criar_backup():
    if not BANCO.exists():
        return None

    PASTA_BACKUPS.mkdir(
        parents=True,
        exist_ok=True
    )

    agora = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    destino = (
        PASTA_BACKUPS
        / f"venda_facil_{agora}.db"
    )

    origem_conn = sqlite3.connect(
        str(BANCO)
    )

    destino_conn = sqlite3.connect(
        str(destino)
    )

    try:
        origem_conn.backup(
            destino_conn
        )

    finally:
        destino_conn.close()
        origem_conn.close()

    limpar_backups_antigos()

    return destino


# =========================================================
# LIMPAR BACKUPS
# =========================================================

def limpar_backups_antigos():
    if not PASTA_BACKUPS.exists():
        return

    backups = sorted(
        PASTA_BACKUPS.glob(
            "venda_facil_*.db"
        ),
        key=lambda arquivo:
            arquivo.stat().st_mtime,
        reverse=True
    )

    for arquivo in backups[
        MAX_BACKUPS:
    ]:
        try:
            arquivo.unlink()

        except OSError:
            pass


# =========================================================
# INTEGRIDADE
# =========================================================

def verificar_integridade():
    if not BANCO.exists():
        return True

    conn = sqlite3.connect(
        str(BANCO)
    )

    try:
        resultado = conn.execute(
            "PRAGMA integrity_check"
        ).fetchone()

        return (
            resultado is not None
            and resultado[0] == "ok"
        )

    finally:
        conn.close()