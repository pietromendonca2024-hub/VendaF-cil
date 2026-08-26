from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QFrame
)

from database import (
    listar_produtos,
    registrar_venda
)


class VendasPage(QWidget):
    def __init__(self):
        super().__init__()

        self.carrinho = {}

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            30,
            30,
            30,
            30
        )

        layout.setSpacing(20)

        # =====================
        # TÍTULO
        # =====================

        titulo = QLabel(
            "Nova Venda"
        )

        titulo.setObjectName(
            "pageTitulo"
        )

        subtitulo = QLabel(
            "Adicione os produtos e finalize a venda."
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

        # =====================
        # ADICIONAR PRODUTO
        # =====================

        adicionar_layout = QHBoxLayout()

        self.produto_combo = QComboBox()

        self.produto_combo.setMinimumHeight(
            42
        )

        self.quantidade = QSpinBox()

        self.quantidade.setMinimum(
            1
        )

        self.quantidade.setMaximum(
            999
        )

        self.quantidade.setValue(
            1
        )

        self.quantidade.setMinimumHeight(
            42
        )

        self.adicionar_btn = QPushButton(
            "Adicionar"
        )

        self.adicionar_btn.setObjectName(
            "primaryButton"
        )

        adicionar_layout.addWidget(
            self.produto_combo,
            4
        )

        adicionar_layout.addWidget(
            self.quantidade,
            1
        )

        adicionar_layout.addWidget(
            self.adicionar_btn
        )

        layout.addLayout(
            adicionar_layout
        )

        # =====================
        # CARRINHO
        # =====================

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            5
        )

        self.tabela.setHorizontalHeaderLabels([
            "Produto",
            "Quantidade",
            "Valor unitário",
            "Subtotal",
            "Ação"
        ])

        self.tabela.verticalHeader().setVisible(
            False
        )

        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
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

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.Fixed
        )

        self.tabela.setColumnWidth(
            4,
            110
        )

        layout.addWidget(
            self.tabela
        )

        # =====================
        # RODAPÉ DA VENDA
        # =====================

        rodape = QFrame()
        rodape.setObjectName(
            "saleFooter"
        )

        rodape_layout = QHBoxLayout(
            rodape
        )

        rodape_layout.setContentsMargins(
            20,
            16,
            20,
            16
        )

        pagamento_layout = QVBoxLayout()

        pagamento_titulo = QLabel(
            "Forma de pagamento"
        )

        pagamento_titulo.setObjectName(
            "fieldLabel"
        )

        self.pagamento_combo = QComboBox()

        self.pagamento_combo.addItems([
            "Pix",
            "Dinheiro",
            "Cartão de débito",
            "Cartão de crédito"
        ])

        self.pagamento_combo.setMinimumHeight(
            42
        )

        self.pagamento_combo.setMinimumWidth(
            190
        )

        pagamento_layout.addWidget(
            pagamento_titulo
        )

        pagamento_layout.addWidget(
            self.pagamento_combo
        )

        total_layout = QVBoxLayout()

        total_texto = QLabel(
            "TOTAL DA VENDA"
        )

        total_texto.setObjectName(
            "totalTitulo"
        )

        self.total_label = QLabel(
            "R$ 0,00"
        )

        self.total_label.setObjectName(
            "totalValor"
        )

        total_layout.addWidget(
            total_texto
        )

        total_layout.addWidget(
            self.total_label
        )

        self.finalizar_btn = QPushButton(
            "Finalizar venda"
        )

        self.finalizar_btn.setObjectName(
            "finishButton"
        )

        self.finalizar_btn.setMinimumHeight(
            50
        )

        rodape_layout.addLayout(
            pagamento_layout
        )

        rodape_layout.addStretch()

        rodape_layout.addLayout(
            total_layout
        )

        rodape_layout.addSpacing(
            25
        )

        rodape_layout.addWidget(
            self.finalizar_btn
        )

        layout.addWidget(
            rodape
        )

        # =====================
        # EVENTOS
        # =====================

        self.adicionar_btn.clicked.connect(
            self.adicionar_produto
        )

        self.finalizar_btn.clicked.connect(
            self.finalizar_venda
        )

        self.carregar_produtos()

    def carregar_produtos(self):
        self.produto_combo.clear()

        produtos = listar_produtos()

        for produto in produtos:
            texto = (
                f"{produto['nome']} - "
                f"R$ {produto['preco']:.2f}"
                .replace(".", ",")
            )

            self.produto_combo.addItem(
                texto,
                produto
            )

    def adicionar_produto(self):
        produto = (
            self.produto_combo.currentData()
        )

        if not produto:
            QMessageBox.warning(
                self,
                "Venda",
                "Nenhum produto disponível."
            )
            return

        quantidade = (
            self.quantidade.value()
        )

        produto_id = produto["id"]

        if produto_id in self.carrinho:
            self.carrinho[
                produto_id
            ]["quantidade"] += quantidade

        else:
            self.carrinho[
                produto_id
            ] = {
                "id": produto["id"],
                "nome": produto["nome"],
                "preco": produto["preco"],
                "quantidade": quantidade
            }

        self.quantidade.setValue(
            1
        )

        self.atualizar_carrinho()

    def atualizar_carrinho(self):
        itens = list(
            self.carrinho.values()
        )

        self.tabela.setRowCount(
            len(itens)
        )

        total = 0

        for linha, item in enumerate(itens):
            self.tabela.setRowHeight(
                linha,
                48
            )

            subtotal = (
                item["preco"]
                * item["quantidade"]
            )

            total += subtotal

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

            preco = (
                f"R$ {item['preco']:.2f}"
                .replace(".", ",")
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    preco
                )
            )

            subtotal_texto = (
                f"R$ {subtotal:.2f}"
                .replace(".", ",")
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    subtotal_texto
                )
            )

            remover_btn = QPushButton(
                "Remover"
            )

            remover_btn.setObjectName(
                "deleteButton"
            )

            remover_btn.setMinimumHeight(
                32
            )

            produto_id = item["id"]

            remover_btn.clicked.connect(
                lambda checked=False,
                pid=produto_id:
                self.remover_item(pid)
            )

            self.tabela.setCellWidget(
                linha,
                4,
                remover_btn
            )

        total_texto = (
            f"R$ {total:.2f}"
            .replace(".", ",")
        )

        self.total_label.setText(
            total_texto
        )

    def remover_item(self, produto_id):
        if produto_id in self.carrinho:
            del self.carrinho[
                produto_id
            ]

        self.atualizar_carrinho()

    def finalizar_venda(self):
        if not self.carrinho:
            QMessageBox.warning(
                self,
                "Venda",
                "Adicione pelo menos um produto."
            )
            return

        forma_pagamento = (
            self.pagamento_combo
            .currentText()
        )

        itens = list(
            self.carrinho.values()
        )

        total = sum(
            item["preco"]
            * item["quantidade"]
            for item in itens
        )

        resposta = QMessageBox.question(
            self,
            "Finalizar venda",
            (
                f"Total: R$ {total:.2f}\n"
                f"Pagamento: {forma_pagamento}\n\n"
                "Confirmar venda?"
            ).replace(".", ","),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if (
            resposta
            != QMessageBox.StandardButton.Yes
        ):
            return

        try:
            venda_id = registrar_venda(
                itens,
                forma_pagamento
            )

            QMessageBox.information(
                self,
                "Venda finalizada",
                (
                    "Venda registrada com sucesso!\n\n"
                    f"Venda #{venda_id}\n"
                    f"Total: R$ {total:.2f}"
                ).replace(".", ",")
            )

            self.carrinho.clear()

            self.atualizar_carrinho()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível registrar a venda.\n{erro}"
            )