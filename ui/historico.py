from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QDialog,
    QMessageBox
)

from PySide6.QtCore import Qt

from database import (
    listar_vendas,
    listar_itens_venda
)


class DetalhesVendaDialog(QDialog):
    def __init__(self, venda_id, parent=None):
        super().__init__(parent)

        self.venda_id = venda_id

        self.setWindowTitle(
            f"Venda #{venda_id}"
        )

        self.resize(
            650,
            420
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            24,
            24,
            24,
            24
        )

        layout.setSpacing(
            18
        )

        titulo = QLabel(
            f"Detalhes da venda #{venda_id}"
        )

        titulo.setObjectName(
            "dialogTitulo"
        )

        subtitulo = QLabel(
            "Produtos registrados nesta venda."
        )

        subtitulo.setObjectName(
            "pageSubtitulo"
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            subtitulo
        )

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            4
        )

        self.tabela.setHorizontalHeaderLabels([
            "Produto",
            "Quantidade",
            "Unitário",
            "Subtotal"
        ])

        self.tabela.verticalHeader().setVisible(
            False
        )

        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        header = self.tabela.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.Stretch
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.ResizeToContents
        )

        layout.addWidget(
            self.tabela
        )

        fechar_btn = QPushButton(
            "Fechar"
        )

        fechar_btn.setObjectName(
            "primaryButton"
        )

        fechar_btn.clicked.connect(
            self.close
        )

        layout.addWidget(
            fechar_btn,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        self.carregar_itens()

    def carregar_itens(self):
        itens = listar_itens_venda(
            self.venda_id
        )

        self.tabela.setRowCount(
            len(itens)
        )

        for linha, item in enumerate(itens):
            self.tabela.setRowHeight(
                linha,
                45
            )

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    item["nome"]
                )
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    str(item["quantidade"])
                )
            )

            unitario = (
                f"R$ {item['preco_unitario']:.2f}"
                .replace(".", ",")
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    unitario
                )
            )

            subtotal = (
                f"R$ {item['subtotal']:.2f}"
                .replace(".", ",")
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    subtotal
                )
            )


class HistoricoPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            30,
            30,
            30,
            30
        )

        layout.setSpacing(
            20
        )

        # =====================
        # CABEÇALHO
        # =====================

        cabecalho = QHBoxLayout()

        textos = QVBoxLayout()

        titulo = QLabel(
            "Histórico"
        )

        titulo.setObjectName(
            "pageTitulo"
        )

        subtitulo = QLabel(
            "Consulte as vendas registradas."
        )

        subtitulo.setObjectName(
            "pageSubtitulo"
        )

        textos.addWidget(
            titulo
        )

        textos.addWidget(
            subtitulo
        )

        self.atualizar_btn = QPushButton(
            "Atualizar"
        )

        self.atualizar_btn.setObjectName(
            "secondaryButton"
        )

        cabecalho.addLayout(
            textos
        )

        cabecalho.addStretch()

        cabecalho.addWidget(
            self.atualizar_btn
        )

        layout.addLayout(
            cabecalho
        )

        # =====================
        # RESUMO
        # =====================

        self.resumo_label = QLabel(
            "0 vendas registradas"
        )

        self.resumo_label.setObjectName(
            "historySummary"
        )

        layout.addWidget(
            self.resumo_label
        )

        # =====================
        # TABELA
        # =====================

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            5
        )

        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Data",
            "Pagamento",
            "Total",
            "Detalhes"
        ])

        self.tabela.verticalHeader().setVisible(
            False
        )

        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        header = self.tabela.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.Fixed
        )

        self.tabela.setColumnWidth(
            4,
            120
        )

        layout.addWidget(
            self.tabela
        )

        # =====================
        # EVENTOS
        # =====================

        self.atualizar_btn.clicked.connect(
            self.carregar_vendas
        )

        self.carregar_vendas()

    def carregar_vendas(self):
        vendas = listar_vendas()

        self.tabela.setRowCount(
            len(vendas)
        )

        self.resumo_label.setText(
            f"{len(vendas)} vendas registradas"
        )

        for linha, venda in enumerate(vendas):
            self.tabela.setRowHeight(
                linha,
                48
            )

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    f"#{venda['id']}"
                )
            )

            data = venda["data"]

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    data
                )
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    venda["forma_pagamento"]
                )
            )

            total = (
                f"R$ {venda['total']:.2f}"
                .replace(".", ",")
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    total
                )
            )

            detalhes_btn = QPushButton(
                "Ver itens"
            )

            detalhes_btn.setObjectName(
                "detailsButton"
            )

            detalhes_btn.setMinimumHeight(
                32
            )

            venda_id = venda["id"]

            detalhes_btn.clicked.connect(
                lambda checked=False, vid=venda_id:
                self.abrir_detalhes(vid)
            )

            self.tabela.setCellWidget(
                linha,
                4,
                detalhes_btn
            )

    def abrir_detalhes(self, venda_id):
        try:
            janela = DetalhesVendaDialog(
                venda_id,
                self
            )

            janela.exec()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível abrir a venda.\n{erro}"
            )