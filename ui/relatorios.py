from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFrame,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView
)

from database import dados_relatorio_mensal


def moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


class RelatorioCard(QFrame):
    def __init__(
        self,
        titulo,
        valor,
        descricao
    ):
        super().__init__()

        self.setObjectName(
            "reportMetricCard"
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            18,
            20,
            18
        )

        layout.setSpacing(
            7
        )

        titulo_label = QLabel(
            titulo.upper()
        )

        titulo_label.setObjectName(
            "reportMetricLabel"
        )

        valor_label = QLabel(
            valor
        )

        valor_label.setObjectName(
            "reportMetricValue"
        )

        descricao_label = QLabel(
            descricao
        )

        descricao_label.setObjectName(
            "reportMetricDescription"
        )

        layout.addWidget(
            titulo_label
        )

        layout.addWidget(
            valor_label
        )

        layout.addWidget(
            descricao_label
        )


class RelatoriosPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            32,
            28,
            32,
            28
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
            "Relatórios"
        )

        titulo.setObjectName(
            "pageTitulo"
        )

        subtitulo = QLabel(
            "Acompanhe o desempenho mensal da loja."
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

        cabecalho.addLayout(
            textos
        )

        cabecalho.addStretch()

        # =====================
        # FILTROS
        # =====================

        self.mes_combo = QComboBox()

        meses = [
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro"
        ]

        for numero, nome in enumerate(
            meses,
            start=1
        ):
            self.mes_combo.addItem(
                nome,
                numero
            )

        self.ano_combo = QComboBox()

        ano_atual = datetime.now().year

        for ano in range(
            ano_atual - 5,
            ano_atual + 2
        ):
            self.ano_combo.addItem(
                str(ano),
                ano
            )

        self.mes_combo.setCurrentIndex(
            datetime.now().month - 1
        )

        indice_ano = self.ano_combo.findData(
            ano_atual
        )

        self.ano_combo.setCurrentIndex(
            indice_ano
        )

        self.atualizar_btn = QPushButton(
            "Gerar relatório"
        )

        self.atualizar_btn.setObjectName(
            "primaryButton"
        )

        cabecalho.addWidget(
            self.mes_combo
        )

        cabecalho.addWidget(
            self.ano_combo
        )

        cabecalho.addWidget(
            self.atualizar_btn
        )

        layout.addLayout(
            cabecalho
        )

        # =====================
        # CONTEÚDO DINÂMICO
        # =====================

        self.conteudo = QVBoxLayout()

        self.conteudo.setSpacing(
            18
        )

        layout.addLayout(
            self.conteudo
        )

        layout.addStretch()

        self.atualizar_btn.clicked.connect(
            self.atualizar_relatorio
        )

        self.mes_combo.currentIndexChanged.connect(
            self.atualizar_relatorio
        )

        self.ano_combo.currentIndexChanged.connect(
            self.atualizar_relatorio
        )

        self.atualizar_relatorio()

    def limpar_layout(
        self,
        layout
    ):
        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()
            sublayout = item.layout()

            if widget:
                widget.deleteLater()

            elif sublayout:
                self.limpar_layout(
                    sublayout
                )

    def atualizar_relatorio(self):
        self.limpar_layout(
            self.conteudo
        )

        mes = self.mes_combo.currentData()
        ano = self.ano_combo.currentData()

        if mes is None or ano is None:
            return

        dados = dados_relatorio_mensal(
            ano,
            mes
        )

        # =====================
        # CARDS
        # =====================

        cards = QHBoxLayout()

        cards.setSpacing(
            15
        )

        cards.addWidget(
            RelatorioCard(
                "Faturamento",
                moeda(
                    dados["faturamento"]
                ),
                "Receita total do mês"
            )
        )

        cards.addWidget(
            RelatorioCard(
                "Vendas",
                str(
                    dados["vendas"]
                ),
                "Vendas realizadas"
            )
        )

        cards.addWidget(
            RelatorioCard(
                "Ticket médio",
                moeda(
                    dados["ticket_medio"]
                ),
                "Média por venda"
            )
        )

        cards.addWidget(
            RelatorioCard(
                "Itens vendidos",
                str(
                    dados["itens_vendidos"]
                ),
                "Unidades comercializadas"
            )
        )

        self.conteudo.addLayout(
            cards
        )

        # =====================
        # GRID
        # =====================

        grid = QGridLayout()

        grid.setHorizontalSpacing(
            18
        )

        grid.setVerticalSpacing(
            18
        )

        painel_pagamentos = (
            self.criar_pagamentos(
                dados["pagamentos"]
            )
        )

        painel_produtos = (
            self.criar_produtos(
                dados["produtos"]
            )
        )

        painel_dias = (
            self.criar_vendas_por_dia(
                dados["vendas_por_dia"]
            )
        )

        grid.addWidget(
            painel_pagamentos,
            0,
            0
        )

        grid.addWidget(
            painel_dias,
            0,
            1
        )

        grid.addWidget(
            painel_produtos,
            1,
            0,
            1,
            2
        )

        grid.setColumnStretch(
            0,
            1
        )

        grid.setColumnStretch(
            1,
            1
        )

        self.conteudo.addLayout(
            grid
        )

    def criar_painel(
        self,
        titulo,
        descricao
    ):
        painel = QFrame()

        painel.setObjectName(
            "reportPanel"
        )

        layout = QVBoxLayout(
            painel
        )

        layout.setContentsMargins(
            20,
            18,
            20,
            18
        )

        layout.setSpacing(
            12
        )

        titulo_label = QLabel(
            titulo
        )

        titulo_label.setObjectName(
            "reportPanelTitle"
        )

        descricao_label = QLabel(
            descricao
        )

        descricao_label.setObjectName(
            "reportPanelDescription"
        )

        layout.addWidget(
            titulo_label
        )

        layout.addWidget(
            descricao_label
        )

        return painel, layout

    def criar_pagamentos(
        self,
        pagamentos
    ):
        painel, layout = self.criar_painel(
            "Formas de pagamento",
            "Valores recebidos no período."
        )

        if not pagamentos:
            vazio = QLabel(
                "Nenhuma venda registrada neste mês."
            )

            vazio.setObjectName(
                "emptyText"
            )

            layout.addWidget(
                vazio
            )

            return painel

        tabela = QTableWidget()

        tabela.setColumnCount(
            3
        )

        tabela.setHorizontalHeaderLabels([
            "Pagamento",
            "Vendas",
            "Total"
        ])

        tabela.setRowCount(
            len(pagamentos)
        )

        self.configurar_tabela(
            tabela
        )

        header = tabela.horizontalHeader()

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

        for linha, pagamento in enumerate(
            pagamentos
        ):
            tabela.setRowHeight(
                linha,
                42
            )

            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    pagamento["forma_pagamento"]
                )
            )

            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    str(
                        pagamento[
                            "quantidade_vendas"
                        ]
                    )
                )
            )

            tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    moeda(
                        pagamento["total"]
                    )
                )
            )

        layout.addWidget(
            tabela
        )

        return painel

    def criar_produtos(
        self,
        produtos
    ):
        painel, layout = self.criar_painel(
            "Produtos vendidos",
            "Quantidade e faturamento de cada item."
        )

        if not produtos:
            vazio = QLabel(
                "Nenhum produto vendido neste mês."
            )

            vazio.setObjectName(
                "emptyText"
            )

            layout.addWidget(
                vazio
            )

            return painel

        tabela = QTableWidget()

        tabela.setColumnCount(
            4
        )

        tabela.setHorizontalHeaderLabels([
            "Posição",
            "Produto",
            "Quantidade",
            "Faturamento"
        ])

        tabela.setRowCount(
            len(produtos)
        )

        self.configurar_tabela(
            tabela
        )

        header = tabela.horizontalHeader()

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

        for linha, produto in enumerate(
            produtos
        ):
            tabela.setRowHeight(
                linha,
                44
            )

            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    f"#{linha + 1}"
                )
            )

            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    produto["nome"]
                )
            )

            tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    str(
                        produto["quantidade"]
                    )
                )
            )

            tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    moeda(
                        produto["faturamento"]
                    )
                )
            )

        tabela.setMinimumHeight(
            220
        )

        layout.addWidget(
            tabela
        )

        return painel

    def criar_vendas_por_dia(
        self,
        vendas
    ):
        painel, layout = self.criar_painel(
            "Movimento diário",
            "Faturamento ao longo do mês."
        )

        if not vendas:
            vazio = QLabel(
                "Nenhuma movimentação encontrada."
            )

            vazio.setObjectName(
                "emptyText"
            )

            layout.addWidget(
                vazio
            )

            return painel

        tabela = QTableWidget()

        tabela.setColumnCount(
            3
        )

        tabela.setHorizontalHeaderLabels([
            "Data",
            "Vendas",
            "Total"
        ])

        tabela.setRowCount(
            len(vendas)
        )

        self.configurar_tabela(
            tabela
        )

        header = tabela.horizontalHeader()

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

        for linha, dia in enumerate(vendas):
            tabela.setRowHeight(
                linha,
                42
            )

            data = dia["dia"]

            if data:
                partes = data.split("-")

                data = (
                    f"{partes[2]}/"
                    f"{partes[1]}/"
                    f"{partes[0]}"
                )

            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    data
                )
            )

            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    str(
                        dia["quantidade"]
                    )
                )
            )

            tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    moeda(
                        dia["total"]
                    )
                )
            )

        layout.addWidget(
            tabela
        )

        return painel

    def configurar_tabela(
        self,
        tabela
    ):
        tabela.verticalHeader().setVisible(
            False
        )

        tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        tabela.setAlternatingRowColors(
            True
        )