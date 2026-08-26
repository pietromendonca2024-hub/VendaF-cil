from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView
)

from database import (
    listar_produtos,
    cadastrar_produto,
    atualizar_produto,
    excluir_produto
)


class ProdutosPage(QWidget):
    def __init__(self):
        super().__init__()

        self.produto_selecionado = None

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

        titulo = QLabel("Produtos")
        titulo.setObjectName("pageTitulo")

        subtitulo = QLabel(
            "Cadastre e gerencie os produtos da loja."
        )
        subtitulo.setObjectName("pageSubtitulo")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # =====================
        # FORMULÁRIO
        # =====================

        formulario = QHBoxLayout()

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText(
            "Nome do produto"
        )

        self.preco_input = QLineEdit()
        self.preco_input.setPlaceholderText(
            "Preço (Ex: 15,90)"
        )

        self.salvar_btn = QPushButton(
            "Adicionar produto"
        )
        self.salvar_btn.setObjectName(
            "primaryButton"
        )

        formulario.addWidget(
            self.nome_input,
            2
        )

        formulario.addWidget(
            self.preco_input,
            1
        )

        formulario.addWidget(
            self.salvar_btn
        )

        layout.addLayout(
            formulario
        )

        # =====================
        # TABELA
        # =====================

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(4)

        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Produto",
            "Preço",
            "Ações"
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
            QHeaderView.ResizeMode.Fixed
        )

        self.tabela.setColumnWidth(
            3,
            170
        )

        layout.addWidget(
            self.tabela
        )

        # =====================
        # EVENTOS
        # =====================

        self.salvar_btn.clicked.connect(
            self.salvar_produto
        )

        self.carregar_produtos()

    def carregar_produtos(self):
        produtos = listar_produtos()

        self.tabela.setRowCount(
            len(produtos)
        )

        for linha, produto in enumerate(produtos):

            self.tabela.setRowHeight(
                linha,
                50
            )

            # ID
            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    str(produto["id"])
                )
            )

            # Produto
            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    produto["nome"]
                )
            )

            # Preço
            preco = (
                f"R$ {produto['preco']:.2f}"
                .replace(".", ",")
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    preco
                )
            )

            # =====================
            # AÇÕES
            # =====================

            acoes = QWidget()

            acoes_layout = QHBoxLayout(
                acoes
            )

            acoes_layout.setContentsMargins(
                4,
                4,
                4,
                4
            )

            acoes_layout.setSpacing(
                6
            )

            editar = QPushButton(
                "Editar"
            )

            excluir = QPushButton(
                "Excluir"
            )

            editar.setObjectName(
                "editButton"
            )

            excluir.setObjectName(
                "deleteButton"
            )

            editar.setMinimumSize(
                65,
                32
            )

            excluir.setMinimumSize(
                65,
                32
            )

            produto_id = produto["id"]

            editar.clicked.connect(
                lambda checked=False, p=produto:
                self.selecionar_produto(p)
            )

            excluir.clicked.connect(
                lambda checked=False, pid=produto_id:
                self.remover_produto(pid)
            )

            acoes_layout.addWidget(
                editar
            )

            acoes_layout.addWidget(
                excluir
            )

            self.tabela.setCellWidget(
                linha,
                3,
                acoes
            )

    def salvar_produto(self):
        nome = (
            self.nome_input
            .text()
            .strip()
        )

        preco_texto = (
            self.preco_input
            .text()
            .strip()
            .replace(",", ".")
        )

        if not nome:
            QMessageBox.warning(
                self,
                "Atenção",
                "Informe o nome do produto."
            )
            return

        try:
            preco = float(
                preco_texto
            )

        except ValueError:
            QMessageBox.warning(
                self,
                "Atenção",
                "Informe um preço válido."
            )
            return

        if preco <= 0:
            QMessageBox.warning(
                self,
                "Atenção",
                "O preço deve ser maior que zero."
            )
            return

        if self.produto_selecionado:

            atualizar_produto(
                self.produto_selecionado,
                nome,
                preco
            )

            QMessageBox.information(
                self,
                "Produto",
                "Produto atualizado com sucesso!"
            )

        else:

            cadastrar_produto(
                nome,
                preco
            )

            QMessageBox.information(
                self,
                "Produto",
                "Produto cadastrado com sucesso!"
            )

        self.limpar_formulario()
        self.carregar_produtos()

    def selecionar_produto(self, produto):
        self.produto_selecionado = (
            produto["id"]
        )

        self.nome_input.setText(
            produto["nome"]
        )

        self.preco_input.setText(
            f"{produto['preco']:.2f}"
            .replace(".", ",")
        )

        self.salvar_btn.setText(
            "Salvar alterações"
        )

    def limpar_formulario(self):
        self.produto_selecionado = None

        self.nome_input.clear()
        self.preco_input.clear()

        self.salvar_btn.setText(
            "Adicionar produto"
        )

    def remover_produto(self, produto_id):
        resposta = QMessageBox.question(
            self,
            "Excluir produto",
            "Deseja realmente excluir este produto?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if (
            resposta
            == QMessageBox.StandardButton.Yes
        ):
            excluir_produto(
                produto_id
            )

            self.limpar_formulario()
            self.carregar_produtos()