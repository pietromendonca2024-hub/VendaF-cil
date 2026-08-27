import os
import sys

from pathlib import Path


# =========================================================
# RECURSOS DO PROGRAMA
# =========================================================

def caminho_recurso(caminho_relativo):
    """
    Localiza arquivos incluídos no programa, como QSS,
    funcionando tanto com python main.py quanto PyInstaller.
    """

    if getattr(sys, "frozen", False):
        base = Path(
            getattr(
                sys,
                "_MEIPASS",
                Path(sys.executable).resolve().parent
            )
        )

    else:
        base = Path(__file__).resolve().parent

    return base / caminho_relativo


# =========================================================
# PASTA DE DADOS DO USUÁRIO
# =========================================================

def pasta_dados():
    """
    Retorna a pasta fixa usada pelo Venda Fácil
    para armazenar banco e backups.

    No Windows:
    C:\\Users\\USUARIO\\AppData\\Local\\VendaFacil
    """

    local_appdata = os.getenv(
        "LOCALAPPDATA"
    )

    if local_appdata:
        pasta = (
            Path(local_appdata)
            / "VendaFacil"
        )

    else:
        pasta = (
            Path.home()
            / ".VendaFacil"
        )

    pasta.mkdir(
        parents=True,
        exist_ok=True
    )

    return pasta


# =========================================================
# BANCO
# =========================================================

def caminho_banco():
    return (
        pasta_dados()
        / "database.db"
    )


# =========================================================
# BACKUPS
# =========================================================

def pasta_backups():
    pasta = (
        pasta_dados()
        / "backups"
    )

    pasta.mkdir(
        parents=True,
        exist_ok=True
    )

    return pasta