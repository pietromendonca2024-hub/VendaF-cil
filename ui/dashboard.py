from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame
)

from database import dados_dashboard


class Card(QFrame):
    def __init__(self, titulo, valor):
        super().__init__()

        self.setObjectName("card")

        layout = QVBoxLayout(self)

        titulo_label = QLabel(titulo)
        titulo_label.setObjectName("cardTitulo")

        valor_label = QLabel(valor)
        valor_label.setObjectName("cardValor")

        layout.addWidget(titulo_label)
        layout.addWidget(valor_label)


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout_principal = QVBoxLayout(self)

        self.layout_principal.setContentsMargins(
            30,
            30,
            30,
            30
        )

        self.layout_principal.setSpacing(25)

        titulo = QLabel("Dashboard")
        titulo.setObjectName("pageTitulo")

        subtitulo = QLabel(
            "Resumo das vendas de hoje."
        )
        subtitulo.setObjectName("pageSubtitulo")

        self.layout_principal.addWidget(titulo)
        self.layout_principal.addWidget(subtitulo)

        self.cards_layout = QHBoxLayout()

        self.layout_principal.addLayout(
            self.cards_layout
        )

        self.layout_principal.addStretch()

        self.atualizar()

    def atualizar(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        dados = dados_dashboard()

        faturamento = (
            f"R$ {dados['faturamento_hoje']:.2f}"
            .replace(".", ",")
        )

        self.cards_layout.addWidget(
            Card(
                "Faturamento hoje",
                faturamento
            )
        )

        self.cards_layout.addWidget(
            Card(
                "Vendas hoje",
                str(dados["vendas_hoje"])
            )
        )

        self.cards_layout.addWidget(
            Card(
                "Itens vendidos",
                str(dados["itens_hoje"])
            )
        )

        self.cards_layout.addWidget(
            Card(
                "Produtos",
                str(dados["total_produtos"])
            )
        )