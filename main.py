import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QMessageBox,
    QDialog
)

from PySide6.QtCore import QSettings

from app_paths import caminho_recurso

from database import (
    criar_banco,
    existe_usuario
)

from services.backup import (
    criar_backup,
    verificar_integridade
)

from ui.dashboard import DashboardPage
from ui.produtos import ProdutosPage
from ui.vendas import VendasPage
from ui.historico import HistoricoPage
from ui.relatorios import RelatoriosPage

from ui.login import (
    LoginDialog,
    CriarAdministradorDialog,
    AlterarSenhaDialog
)


class VendaFacil(QMainWindow):

    def __init__(self, usuario_logado):
        super().__init__()

        self.usuario_logado = usuario_logado

        # =====================
        # CONFIGURAÇÕES
        # =====================

        self.config = QSettings(
            "VendaFacil",
            "VendaFacil"
        )

        self.tema_escuro = (
            self.config.value(
                "tema",
                "claro"
            ) == "escuro"
        )

        # =====================
        # JANELA
        # =====================

        self.setWindowTitle(
            "Venda Fácil"
        )

        self.resize(
            1280,
            760
        )

        self.setMinimumSize(
            1000,
            620
        )

        container = QWidget()

        self.setCentralWidget(
            container
        )

        layout = QHBoxLayout(
            container
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(0)

        # =====================
        # SIDEBAR
        # =====================

        sidebar = QWidget()

        sidebar.setObjectName(
            "sidebar"
        )

        sidebar.setFixedWidth(
            240
        )

        sidebar_layout = QVBoxLayout(
            sidebar
        )

        sidebar_layout.setContentsMargins(
            20,
            30,
            20,
            24
        )

        sidebar_layout.setSpacing(
            8
        )

        # =====================
        # LOGO
        # =====================

        logo = QLabel(
            "Venda Fácil"
        )

        logo.setObjectName(
            "logo"
        )

        descricao = QLabel(
            "GESTÃO DE VENDAS"
        )

        descricao.setObjectName(
            "logoDescricao"
        )

        sidebar_layout.addWidget(
            logo
        )

        sidebar_layout.addWidget(
            descricao
        )

        sidebar_layout.addSpacing(
            35
        )

        # =====================
        # MENU
        # =====================

        self.btn_dashboard = QPushButton(
            "⌂   Dashboard"
        )

        self.btn_vendas = QPushButton(
            "＋   Nova Venda"
        )

        self.btn_produtos = QPushButton(
            "▣   Produtos"
        )

        self.btn_historico = QPushButton(
            "◷   Histórico"
        )

        self.btn_relatorios = QPushButton(
            "▤   Relatórios"
        )

        self.botoes_menu = [
            self.btn_dashboard,
            self.btn_vendas,
            self.btn_produtos,
            self.btn_historico,
            self.btn_relatorios
        ]

        for botao in self.botoes_menu:
            botao.setObjectName(
                "menuButton"
            )

            botao.setCheckable(
                True
            )

            botao.setMinimumHeight(
                44
            )

            sidebar_layout.addWidget(
                botao
            )

        sidebar_layout.addStretch()

        # =====================
        # USUÁRIO
        # =====================

        usuario_titulo = QLabel(
            "USUÁRIO"
        )

        usuario_titulo.setObjectName(
            "userLabel"
        )

        self.usuario_label = QLabel(
            self.usuario_logado[
                "usuario"
            ]
        )

        self.usuario_label.setObjectName(
            "userName"
        )

        sidebar_layout.addWidget(
            usuario_titulo
        )

        sidebar_layout.addWidget(
            self.usuario_label
        )

        sidebar_layout.addSpacing(
            10
        )

        # =====================
        # ALTERAR SENHA
        # =====================

        self.btn_senha = QPushButton(
            "⚿   Alterar senha"
        )

        self.btn_senha.setObjectName(
            "themeButton"
        )

        self.btn_senha.setMinimumHeight(
            40
        )

        sidebar_layout.addWidget(
            self.btn_senha
        )

        sidebar_layout.addSpacing(
            6
        )

        # =====================
        # TEMA
        # =====================

        self.btn_tema = QPushButton()

        self.btn_tema.setObjectName(
            "themeButton"
        )

        self.btn_tema.setMinimumHeight(
            40
        )

        sidebar_layout.addWidget(
            self.btn_tema
        )

        sidebar_layout.addSpacing(
            10
        )

        # =====================
        # VERSÃO
        # =====================

        versao = QLabel(
            "Venda Fácil\nv0.3.1"
        )

        versao.setObjectName(
            "versao"
        )

        sidebar_layout.addWidget(
            versao
        )

        # =====================
        # PÁGINAS
        # =====================

        self.paginas = QStackedWidget()

        self.dashboard = DashboardPage()

        self.pagina_vendas = VendasPage()

        self.pagina_produtos = ProdutosPage()

        self.pagina_historico = HistoricoPage()

        self.pagina_relatorios = RelatoriosPage()

        self.paginas.addWidget(
            self.dashboard
        )

        self.paginas.addWidget(
            self.pagina_vendas
        )

        self.paginas.addWidget(
            self.pagina_produtos
        )

        self.paginas.addWidget(
            self.pagina_historico
        )

        self.paginas.addWidget(
            self.pagina_relatorios
        )

        # =====================
        # LAYOUT
        # =====================

        layout.addWidget(
            sidebar
        )

        layout.addWidget(
            self.paginas,
            1
        )

        # =====================
        # EVENTOS
        # =====================

        self.btn_dashboard.clicked.connect(
            self.abrir_dashboard
        )

        self.btn_vendas.clicked.connect(
            self.abrir_vendas
        )

        self.btn_produtos.clicked.connect(
            self.abrir_produtos
        )

        self.btn_historico.clicked.connect(
            self.abrir_historico
        )

        self.btn_relatorios.clicked.connect(
            self.abrir_relatorios
        )

        self.btn_senha.clicked.connect(
            self.abrir_alterar_senha
        )

        self.btn_tema.clicked.connect(
            self.alternar_tema
        )

        # =====================
        # INICIAR
        # =====================

        self.aplicar_tema_atual()

        self.abrir_dashboard()

    # =========================
    # MENU ATIVO
    # =========================

    def marcar_menu(
        self,
        botao_ativo
    ):
        for botao in self.botoes_menu:
            botao.setChecked(
                botao == botao_ativo
            )

    # =========================
    # DASHBOARD
    # =========================

    def abrir_dashboard(self):
        self.dashboard.atualizar()

        self.paginas.setCurrentIndex(
            0
        )

        self.marcar_menu(
            self.btn_dashboard
        )

    # =========================
    # VENDAS
    # =========================

    def abrir_vendas(self):
        self.pagina_vendas.carregar_produtos()

        self.paginas.setCurrentIndex(
            1
        )

        self.marcar_menu(
            self.btn_vendas
        )

    # =========================
    # PRODUTOS
    # =========================

    def abrir_produtos(self):
        self.pagina_produtos.carregar_produtos()

        self.paginas.setCurrentIndex(
            2
        )

        self.marcar_menu(
            self.btn_produtos
        )

    # =========================
    # HISTÓRICO
    # =========================

    def abrir_historico(self):
        self.pagina_historico.carregar_vendas()

        self.paginas.setCurrentIndex(
            3
        )

        self.marcar_menu(
            self.btn_historico
        )

    # =========================
    # RELATÓRIOS
    # =========================

    def abrir_relatorios(self):
        self.pagina_relatorios.atualizar_relatorio()

        self.paginas.setCurrentIndex(
            4
        )

        self.marcar_menu(
            self.btn_relatorios
        )

    # =========================
    # ALTERAR SENHA
    # =========================

    def abrir_alterar_senha(self):
        janela = AlterarSenhaDialog(
            self.usuario_logado[
                "id"
            ],
            self
        )

        janela.exec()

    # =========================
    # TEMA
    # =========================

    def aplicar_tema_atual(self):
        app = QApplication.instance()

        if self.tema_escuro:
            arquivo_tema = caminho_recurso(
                "assets/dark.qss"
            )

            self.btn_tema.setText(
                "☀   Modo claro"
            )

        else:
            arquivo_tema = caminho_recurso(
                "assets/style.qss"
            )

            self.btn_tema.setText(
                "☾   Modo escuro"
            )

        try:
            with open(
                arquivo_tema,
                "r",
                encoding="utf-8"
            ) as arquivo:
                app.setStyleSheet(
                    arquivo.read()
                )

        except FileNotFoundError:
            QMessageBox.warning(
                self,
                "Tema",
                (
                    "O arquivo de tema "
                    "não foi encontrado.\n\n"
                    f"{arquivo_tema}"
                )
            )

    def alternar_tema(self):
        self.tema_escuro = (
            not self.tema_escuro
        )

        if self.tema_escuro:
            self.config.setValue(
                "tema",
                "escuro"
            )

        else:
            self.config.setValue(
                "tema",
                "claro"
            )

        self.config.sync()

        self.aplicar_tema_atual()

    # =========================
    # FECHAR / BACKUP
    # =========================

    def closeEvent(
        self,
        event
    ):
        try:
            criar_backup()

            event.accept()

        except Exception as erro:
            resposta = QMessageBox.warning(
                self,
                "Falha no backup",
                (
                    "Não foi possível criar "
                    "o backup antes de fechar."
                    "\n\n"
                    f"Erro: {erro}"
                    "\n\n"
                    "Deseja fechar mesmo assim?"
                ),
                QMessageBox.StandardButton.Yes
                |
                QMessageBox.StandardButton.No
            )

            if resposta == (
                QMessageBox.StandardButton.Yes
            ):
                event.accept()

            else:
                event.ignore()


# =========================================================
# TEMA ANTES DO LOGIN
# =========================================================

def carregar_tema_inicial(app):
    config = QSettings(
        "VendaFacil",
        "VendaFacil"
    )

    escuro = (
        config.value(
            "tema",
            "claro"
        ) == "escuro"
    )

    if escuro:
        arquivo_tema = caminho_recurso(
            "assets/dark.qss"
        )

    else:
        arquivo_tema = caminho_recurso(
            "assets/style.qss"
        )

    try:
        with open(
            arquivo_tema,
            "r",
            encoding="utf-8"
        ) as arquivo:
            app.setStyleSheet(
                arquivo.read()
            )

    except FileNotFoundError:
        print(
            "Tema não encontrado:",
            arquivo_tema
        )


# =========================================================
# INICIAR
# =========================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "Venda Fácil"
    )

    carregar_tema_inicial(
        app
    )

    # =====================
    # BANCO
    # =====================

    criar_banco()

    # =====================
    # INTEGRIDADE
    # =====================

    if not verificar_integridade():
        QMessageBox.critical(
            None,
            "Erro no banco de dados",
            (
                "O banco de dados não passou "
                "na verificação de integridade."
                "\n\n"
                "Por segurança, o Venda Fácil "
                "não será iniciado."
            )
        )

        sys.exit(
            1
        )

    # =====================
    # BACKUP INICIAL
    # =====================

    try:
        criar_backup()

    except Exception as erro:
        QMessageBox.warning(
            None,
            "Backup",
            (
                "O sistema não conseguiu criar "
                "o backup inicial."
                "\n\n"
                f"{erro}"
            )
        )

    # =====================
    # PRIMEIRO ACESSO
    # =====================

    if not existe_usuario():
        configuracao = (
            CriarAdministradorDialog()
        )

        resultado = (
            configuracao.exec()
        )

        if resultado != (
            QDialog.DialogCode.Accepted
        ):
            sys.exit(
                0
            )

    # =====================
    # LOGIN
    # =====================

    login = LoginDialog()

    resultado = login.exec()

    if resultado != (
        QDialog.DialogCode.Accepted
    ):
        sys.exit(
            0
        )

    # =====================
    # ABRIR SISTEMA
    # =====================

    janela = VendaFacil(
        login.usuario_logado
    )

    janela.show()

    sys.exit(
        app.exec()
    )