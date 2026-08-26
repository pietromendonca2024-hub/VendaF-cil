import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget
)

from database import criar_banco
from ui.dashboard import DashboardPage
from ui.produtos import ProdutosPage
from ui.vendas import VendasPage


class PlaceholderPage(QWidget):
    def __init__(self, titulo):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            30,
            30,
            30,
            30
        )

        label = QLabel(titulo)
        label.setObjectName("pageTitulo")

        texto = QLabel(
            "Esta área será implementada na próxima etapa."
        )
        texto.setObjectName("pageSubtitulo")

        layout.addWidget(label)
        layout.addWidget(texto)

        layout.addStretch()


class VendaFacil(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Venda Fácil")

        self.resize(
            1200,
            720
        )

        self.setMinimumSize(
            950,
            600
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
        sidebar.setObjectName("sidebar")

        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(
            sidebar
        )

        sidebar_layout.setContentsMargins(
            20,
            28,
            20,
            28
        )

        sidebar_layout.setSpacing(8)

        logo = QLabel("Venda Fácil")
        logo.setObjectName("logo")

        descricao = QLabel(
            "Sistema de Vendas"
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

        self.btn_dashboard = QPushButton(
            "Dashboard"
        )

        self.btn_vendas = QPushButton(
            "Nova Venda"
        )

        self.btn_produtos = QPushButton(
            "Produtos"
        )

        self.btn_historico = QPushButton(
            "Histórico"
        )

        self.btn_relatorios = QPushButton(
            "Relatórios"
        )

        botoes = [
            self.btn_dashboard,
            self.btn_vendas,
            self.btn_produtos,
            self.btn_historico,
            self.btn_relatorios
        ]

        for botao in botoes:
            botao.setObjectName(
                "menuButton"
            )

            sidebar_layout.addWidget(
                botao
            )

        sidebar_layout.addStretch()

        versao = QLabel(
            "Venda Fácil v0.1"
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

        self.pagina_historico = PlaceholderPage(
            "Histórico"
        )

        self.pagina_relatorios = PlaceholderPage(
            "Relatórios"
        )

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

        layout.addWidget(
            sidebar
        )

        layout.addWidget(
            self.paginas
        )

        # =====================
        # BOTÕES
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
            lambda: self.paginas.setCurrentIndex(3)
        )

        self.btn_relatorios.clicked.connect(
            lambda: self.paginas.setCurrentIndex(4)
        )

    def abrir_dashboard(self):
        self.dashboard.atualizar()

        self.paginas.setCurrentIndex(
            0
        )
    def abrir_vendas(self):
        self.pagina_vendas.carregar_produtos()

        self.paginas.setCurrentIndex(
            1
        )
    def abrir_produtos(self):
        self.pagina_produtos.carregar_produtos()

        self.paginas.setCurrentIndex(
            2
        )


def aplicar_estilo(app):
    app.setStyleSheet("""
        QMainWindow {
            background: #f4f6f9;
        }

        QWidget {
            font-family: "Segoe UI";
            font-size: 14px;
            color: #0f172a;
        }

        /* SIDEBAR */

        #sidebar {
            background: #0f172a;
        }

        #logo {
            color: white;
            font-size: 25px;
            font-weight: 700;
        }

        #logoDescricao {
            color: #64748b;
            font-size: 12px;
        }

        #menuButton {
            background: transparent;
            color: #cbd5e1;

            border: none;
            border-radius: 8px;

            padding: 12px 14px;

            text-align: left;

            font-size: 14px;
        }

        #menuButton:hover {
            background: #1e293b;
            color: white;
        }

        #menuButton:pressed {
            background: #2563eb;
            color: white;
        }

        #versao {
            color: #475569;
            font-size: 11px;
        }

        /* TÍTULOS */

        #pageTitulo {
            font-size: 30px;
            font-weight: 700;
            color: #0f172a;
        }

        #pageSubtitulo {
            color: #64748b;
            font-size: 14px;
        }

        /* DASHBOARD */

        #card {
            background: white;

            border: 1px solid #e2e8f0;

            border-radius: 14px;

            padding: 15px;

            min-height: 110px;
        }

        #cardTitulo {
            color: #64748b;
            font-size: 13px;
        }

        #cardValor {
            color: #0f172a;

            font-size: 27px;
            font-weight: 700;
        }

        /* CAMPOS */

        QLineEdit {
            background: white;

            border: 1px solid #dbe2ea;

            border-radius: 8px;

            padding: 11px;

            font-size: 14px;
        }

        QLineEdit:focus {
            border: 1px solid #2563eb;
        }

        /* TABELA */

        QTableWidget {
            background: white;

            border: 1px solid #e2e8f0;

            border-radius: 10px;

            gridline-color: #f1f5f9;

            selection-background-color: #eff6ff;
            selection-color: #0f172a;
        }

        QTableWidget::item {
            padding: 8px;
        }

        QHeaderView::section {
            background: #f8fafc;

            color: #64748b;

            border: none;

            border-bottom: 1px solid #e2e8f0;

            padding: 10px;

            font-weight: 600;
        }

        /* BOTÃO PRINCIPAL */

        #primaryButton {
            background: #2563eb;

            color: white;

            border: none;

            border-radius: 8px;

            padding: 11px 18px;

            font-weight: 600;
        }

        #primaryButton:hover {
            background: #1d4ed8;
        }

        /* EDITAR */

        #editButton {
            background: #eff6ff;

            color: #2563eb;

            border: none;

            border-radius: 6px;

            padding: 7px 12px;
        }

        #editButton:hover {
            background: #dbeafe;
        }

        /* EXCLUIR */

        #deleteButton {
            background: #fef2f2;

            color: #dc2626;

            border: none;

            border-radius: 6px;

            padding: 7px 12px;
        }

        #deleteButton:hover {
            background: #fee2e2;
        }
        QComboBox,
QSpinBox {
    background: white;

    border: 1px solid #dbe2ea;

    border-radius: 8px;

    padding: 9px;

    font-size: 14px;
}

QComboBox:focus,
QSpinBox:focus {
    border: 1px solid #2563eb;
}

#saleFooter {
    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 12px;
}

#fieldLabel {
    color: #64748b;

    font-size: 12px;

    font-weight: 600;
}

#totalTitulo {
    color: #64748b;

    font-size: 11px;

    font-weight: 600;
}

#totalValor {
    color: #0f172a;

    font-size: 26px;

    font-weight: 700;
}

#finishButton {
    background: #16a34a;

    color: white;

    border: none;

    border-radius: 9px;

    padding: 12px 22px;

    font-size: 14px;

    font-weight: 700;
}

#finishButton:hover {
    background: #15803d;
}
    """)


if __name__ == "__main__":
    criar_banco()

    app = QApplication(
        sys.argv
    )

    aplicar_estilo(
        app
    )

    janela = VendaFacil()

    janela.show()

    sys.exit(
        app.exec()
    )