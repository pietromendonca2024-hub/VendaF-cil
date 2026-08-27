from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView
)

from database import dados_dashboard


def moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


class MetricCard(QFrame):
    def __init__(
        self,
        titulo,
        valor,
        descricao
    ):
        super().__init__()

        self.setObjectName(
            "metricCard"
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            18,
            20,
            18
        )

        layout.setSpacing(
            8
        )

        titulo_label = QLabel(
            titulo.upper()
        )

        titulo_label.setObjectName(
            "metricLabel"
        )

        valor_label = QLabel(
            valor
        )

        valor_label.setObjectName(
            "metricValue"
        )

        descricao_label = QLabel(
            descricao
        )

        descricao_label.setObjectName(
            "metricDescription"
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


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout_principal = QVBoxLayout(
            self
        )

        self.layout_principal.setContentsMargins(
            32,
            28,
            32,
            28
        )

        self.layout_principal.setSpacing(
            22
        )

        # =====================
        # CABEÇALHO
        # =====================

        header = QHBoxLayout()

        header_textos = QVBoxLayout()

        titulo = QLabel(
            "Dashboard"
        )

        titulo.setObjectName(
            "pageTitulo"
        )

        subtitulo = QLabel(
            "Acompanhe o movimento da loja em tempo real."
        )

        subtitulo.setObjectName(
            "pageSubtitulo"
        )

        header_textos.addWidget(
            titulo
        )

        header_textos.addWidget(
            subtitulo
        )

        self.data_label = QLabel()

        self.data_label.setObjectName(
            "dashboardDate"
        )

        header.addLayout(
            header_textos
        )

        header.addStretch()

        header.addWidget(
            self.data_label
        )

        self.layout_principal.addLayout(
            header
        )

        # =====================
        # ÁREA DINÂMICA
        # =====================

        self.conteudo = QVBoxLayout()

        self.conteudo.setSpacing(
            20
        )

        self.layout_principal.addLayout(
            self.conteudo
        )

        self.layout_principal.addStretch()

        self.atualizar()

    def limpar_layout(self, layout):
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

    def atualizar(self):
        self.limpar_layout(
            self.conteudo
        )

        dados = dados_dashboard()

        agora = datetime.now()

        dias = [
            "segunda-feira",
            "terça-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sábado",
            "domingo"
        ]

        meses = [
            "janeiro",
            "fevereiro",
            "março",
            "abril",
            "maio",
            "junho",
            "julho",
            "agosto",
            "setembro",
            "outubro",
            "novembro",
            "dezembro"
        ]

        texto_data = (
            f"{dias[agora.weekday()]}, "
            f"{agora.day} de "
            f"{meses[agora.month - 1]}"
        )

        self.data_label.setText(
            texto_data.capitalize()
        )

        # =====================
        # MÉTRICAS
        # =====================

        cards = QHBoxLayout()

        cards.setSpacing(
            16
        )

        cards.addWidget(
            MetricCard(
                "Faturamento",
                moeda(
                    dados["faturamento_hoje"]
                ),
                "Receita de hoje"
            )
        )

        cards.addWidget(
            MetricCard(
                "Vendas",
                str(
                    dados["vendas_hoje"]
                ),
                "Pedidos finalizados"
            )
        )

        cards.addWidget(
            MetricCard(
                "Ticket médio",
                moeda(
                    dados["ticket_medio"]
                ),
                "Valor médio por venda"
            )
        )

        cards.addWidget(
            MetricCard(
                "Itens vendidos",
                str(
                    dados["itens_hoje"]
                ),
                "Unidades vendidas hoje"
            )
        )

        self.conteudo.addLayout(
            cards
        )

        # =====================
        # GRID PRINCIPAL
        # =====================

        grid = QGridLayout()

        grid.setHorizontalSpacing(
            18
        )

        grid.setVerticalSpacing(
            18
        )

        pagamentos = self.criar_pagamentos(
            dados["pagamentos"]
        )

        vendas = self.criar_ultimas_vendas(
            dados["ultimas_vendas"]
        )

        destaque = self.criar_destaque(
            dados["produto_mais_vendido"]
        )

        produtos = self.criar_produtos_card(
            dados["total_produtos"]
        )

        grid.addWidget(
            pagamentos,
            0,
            0
        )

        grid.addWidget(
            vendas,
            0,
            1
        )

        grid.addWidget(
            destaque,
            1,
            0
        )

        grid.addWidget(
            produtos,
            1,
            1
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
            "dashboardPanel"
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
            14
        )

        titulo_label = QLabel(
            titulo
        )

        titulo_label.setObjectName(
            "panelTitle"
        )

        descricao_label = QLabel(
            descricao
        )

        descricao_label.setObjectName(
            "panelDescription"
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
            "Recebimentos registrados hoje."
        )

        if not pagamentos:
            vazio = QLabel(
                "Nenhum recebimento hoje."
            )

            vazio.setObjectName(
                "emptyText"
            )

            layout.addWidget(
                vazio
            )

            return painel

        for pagamento in pagamentos:

            linha = QFrame()

            linha.setObjectName(
                "paymentRow"
            )

            linha_layout = QHBoxLayout(
                linha
            )

            linha_layout.setContentsMargins(
                12,
                10,
                12,
                10
            )

            nome = QLabel(
                pagamento["forma_pagamento"]
            )

            nome.setObjectName(
                "paymentName"
            )

            valor = QLabel(
                moeda(
                    pagamento["total"]
                )
            )

            valor.setObjectName(
                "paymentValue"
            )

            linha_layout.addWidget(
                nome
            )

            linha_layout.addStretch()

            linha_layout.addWidget(
                valor
            )

            layout.addWidget(
                linha
            )

        return painel

    def criar_ultimas_vendas(
        self,
        vendas
    ):
        painel, layout = self.criar_painel(
            "Últimas vendas",
            "Movimentações mais recentes."
        )

        tabela = QTableWidget()

        tabela.setColumnCount(
            3
        )

        tabela.setHorizontalHeaderLabels([
            "Venda",
            "Pagamento",
            "Total"
        ])

        tabela.verticalHeader().setVisible(
            False
        )

        tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        tabela.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )

        tabela.setFocusPolicy(
            tabela.focusPolicy()
        )

        tabela.setRowCount(
            len(vendas)
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

        for linha, venda in enumerate(vendas):

            tabela.setRowHeight(
                linha,
                40
            )

            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    f"#{venda['id']}"
                )
            )

            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    venda["forma_pagamento"]
                )
            )

            tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    moeda(
                        venda["total"]
                    )
                )
            )

        tabela.setMinimumHeight(
            215
        )

        layout.addWidget(
            tabela
        )

        return painel

    def criar_destaque(
        self,
        produto
    ):
        painel, layout = self.criar_painel(
            "Produto destaque",
            "Item com maior saída hoje."
        )

        if produto:

            nome = QLabel(
                produto["nome"]
            )

            nome.setObjectName(
                "highlightValue"
            )

            quantidade = QLabel(
                f"{produto['quantidade']} unidades vendidas"
            )

            quantidade.setObjectName(
                "highlightDescription"
            )

        else:

            nome = QLabel(
                "Nenhuma venda"
            )

            nome.setObjectName(
                "highlightValue"
            )

            quantidade = QLabel(
                "O destaque aparecerá após as vendas."
            )

            quantidade.setObjectName(
                "highlightDescription"
            )

        layout.addStretch()

        layout.addWidget(
            nome
        )

        layout.addWidget(
            quantidade
        )

        layout.addStretch()

        return painel

    def criar_produtos_card(
        self,
        quantidade
    ):
        painel, layout = self.criar_painel(
            "Catálogo",
            "Produtos disponíveis para venda."
        )

        numero = QLabel(
            str(quantidade)
        )

        numero.setObjectName(
            "highlightValue"
        )

        texto = QLabel(
            "produtos ativos"
        )

        texto.setObjectName(
            "highlightDescription"
        )

        layout.addStretch()

        layout.addWidget(
            numero
        )

        layout.addWidget(
            texto
        )

        layout.addStretch()

        return painel

    