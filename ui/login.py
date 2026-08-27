from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from PySide6.QtCore import (
    Qt,
    QTimer
)

from database import (
    cadastrar_usuario,
    autenticar_usuario,
    alterar_senha
)


# =========================================================
# PRIMEIRO ACESSO
# =========================================================

class CriarAdministradorDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):
        super().__init__(
            parent
        )

        self.setWindowTitle(
            "Configuração inicial"
        )

        self.setFixedSize(
            440,
            500
        )

        self.setModal(
            True
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            45,
            40,
            45,
            40
        )

        layout.setSpacing(
            14
        )

        logo = QLabel(
            "Venda Fácil"
        )

        logo.setObjectName(
            "loginLogo"
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        titulo = QLabel(
            "Criar administrador"
        )

        titulo.setObjectName(
            "loginTitle"
        )

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        descricao = QLabel(
            "Configure a conta responsável "
            "pelo sistema."
        )

        descricao.setObjectName(
            "loginDescription"
        )

        descricao.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        descricao.setWordWrap(
            True
        )

        layout.addWidget(
            logo
        )

        layout.addSpacing(
            5
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            descricao
        )

        layout.addSpacing(
            15
        )

        # =====================
        # USUÁRIO
        # =====================

        usuario_label = QLabel(
            "USUÁRIO"
        )

        usuario_label.setObjectName(
            "loginFieldLabel"
        )

        self.usuario_input = (
            QLineEdit()
        )

        self.usuario_input.setPlaceholderText(
            "Ex: administrador"
        )

        self.usuario_input.setMinimumHeight(
            44
        )

        layout.addWidget(
            usuario_label
        )

        layout.addWidget(
            self.usuario_input
        )

        # =====================
        # SENHA
        # =====================

        senha_label = QLabel(
            "SENHA"
        )

        senha_label.setObjectName(
            "loginFieldLabel"
        )

        self.senha_input = (
            QLineEdit()
        )

        self.senha_input.setPlaceholderText(
            "8+ caracteres, letra e número"
        )

        self.senha_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.senha_input.setMinimumHeight(
            44
        )

        layout.addWidget(
            senha_label
        )

        layout.addWidget(
            self.senha_input
        )

        # =====================
        # CONFIRMAÇÃO
        # =====================

        confirmar_label = QLabel(
            "CONFIRMAR SENHA"
        )

        confirmar_label.setObjectName(
            "loginFieldLabel"
        )

        self.confirmar_input = (
            QLineEdit()
        )

        self.confirmar_input.setPlaceholderText(
            "Repita a senha"
        )

        self.confirmar_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.confirmar_input.setMinimumHeight(
            44
        )

        layout.addWidget(
            confirmar_label
        )

        layout.addWidget(
            self.confirmar_input
        )

        layout.addStretch()

        self.criar_btn = QPushButton(
            "Criar administrador"
        )

        self.criar_btn.setObjectName(
            "loginButton"
        )

        self.criar_btn.setMinimumHeight(
            46
        )

        layout.addWidget(
            self.criar_btn
        )

        self.criar_btn.clicked.connect(
            self.criar_conta
        )

        self.confirmar_input.returnPressed.connect(
            self.criar_conta
        )

    def criar_conta(self):
        usuario = (
            self.usuario_input
            .text()
            .strip()
        )

        senha = (
            self.senha_input.text()
        )

        confirmar = (
            self.confirmar_input.text()
        )

        if senha != confirmar:

            QMessageBox.warning(
                self,
                "Senhas diferentes",
                (
                    "A senha e a confirmação "
                    "não são iguais."
                )
            )

            return

        try:
            cadastrar_usuario(
                usuario,
                senha
            )

        except ValueError as erro:

            QMessageBox.warning(
                self,
                "Não foi possível criar",
                str(erro)
            )

            return

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                (
                    "Não foi possível criar "
                    "o administrador.\n\n"
                    f"{erro}"
                )
            )

            return

        QMessageBox.information(
            self,
            "Administrador criado",
            (
                "A conta foi criada "
                "com sucesso."
            )
        )

        self.accept()


# =========================================================
# LOGIN
# =========================================================

class LoginDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):
        super().__init__(
            parent
        )

        self.usuario_logado = None

        self.segundos_bloqueio = 0

        self.timer_bloqueio = QTimer(
            self
        )

        self.timer_bloqueio.timeout.connect(
            self.atualizar_bloqueio
        )

        self.setWindowTitle(
            "Venda Fácil - Login"
        )

        self.setFixedSize(
            420,
            455
        )

        self.setModal(
            True
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            45,
            40,
            45,
            40
        )

        layout.setSpacing(
            14
        )

        logo = QLabel(
            "Venda Fácil"
        )

        logo.setObjectName(
            "loginLogo"
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitulo = QLabel(
            "GESTÃO DE VENDAS"
        )

        subtitulo.setObjectName(
            "loginSubtitle"
        )

        subtitulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            logo
        )

        layout.addWidget(
            subtitulo
        )

        layout.addSpacing(
            20
        )

        titulo = QLabel(
            "Acesso ao sistema"
        )

        titulo.setObjectName(
            "loginTitle"
        )

        descricao = QLabel(
            "Informe suas credenciais "
            "para continuar."
        )

        descricao.setObjectName(
            "loginDescription"
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            descricao
        )

        layout.addSpacing(
            8
        )

        # =====================
        # USUÁRIO
        # =====================

        usuario_label = QLabel(
            "USUÁRIO"
        )

        usuario_label.setObjectName(
            "loginFieldLabel"
        )

        self.usuario_input = (
            QLineEdit()
        )

        self.usuario_input.setPlaceholderText(
            "Digite seu usuário"
        )

        self.usuario_input.setMinimumHeight(
            44
        )

        layout.addWidget(
            usuario_label
        )

        layout.addWidget(
            self.usuario_input
        )

        # =====================
        # SENHA
        # =====================

        senha_label = QLabel(
            "SENHA"
        )

        senha_label.setObjectName(
            "loginFieldLabel"
        )

        self.senha_input = (
            QLineEdit()
        )

        self.senha_input.setPlaceholderText(
            "Digite sua senha"
        )

        self.senha_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.senha_input.setMinimumHeight(
            44
        )

        layout.addWidget(
            senha_label
        )

        layout.addWidget(
            self.senha_input
        )

        # =====================
        # STATUS
        # =====================

        self.status_label = QLabel(
            ""
        )

        self.status_label.setObjectName(
            "loginDescription"
        )

        self.status_label.setWordWrap(
            True
        )

        layout.addWidget(
            self.status_label
        )

        layout.addStretch()

        self.login_btn = QPushButton(
            "Entrar"
        )

        self.login_btn.setObjectName(
            "loginButton"
        )

        self.login_btn.setMinimumHeight(
            46
        )

        layout.addWidget(
            self.login_btn
        )

        self.login_btn.clicked.connect(
            self.fazer_login
        )

        self.senha_input.returnPressed.connect(
            self.fazer_login
        )

        self.usuario_input.setFocus()

    # =====================================================
    # LOGIN
    # =====================================================

    def fazer_login(self):
        usuario = (
            self.usuario_input
            .text()
            .strip()
        )

        senha = (
            self.senha_input
            .text()
        )

        if not usuario or not senha:

            QMessageBox.warning(
                self,
                "Login",
                (
                    "Informe o usuário "
                    "e a senha."
                )
            )

            return

        try:
            resultado = autenticar_usuario(
                usuario,
                senha
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                (
                    "Não foi possível verificar "
                    "as credenciais.\n\n"
                    f"{erro}"
                )
            )

            return

        # =====================
        # LOGIN CORRETO
        # =====================

        if resultado.get(
            "sucesso"
        ):
            self.usuario_logado = (
                resultado["usuario"]
            )

            self.accept()

            return

        motivo = resultado.get(
            "motivo"
        )

        # =====================
        # BLOQUEADO
        # =====================

        if motivo == "bloqueado":
            self.segundos_bloqueio = (
                resultado.get(
                    "segundos",
                    300
                )
            )

            self.iniciar_bloqueio()

            return

        # =====================
        # CREDENCIAIS ERRADAS
        # =====================

        restantes = resultado.get(
            "tentativas_restantes"
        )

        mensagem = (
            "Usuário ou senha incorretos."
        )

        if restantes is not None:
            mensagem += (
                f"\n\nTentativas restantes: "
                f"{restantes}"
            )

        QMessageBox.warning(
            self,
            "Acesso negado",
            mensagem
        )

        self.senha_input.clear()

        self.senha_input.setFocus()

    # =====================================================
    # BLOQUEIO
    # =====================================================

    def iniciar_bloqueio(self):
        self.login_btn.setEnabled(
            False
        )

        self.usuario_input.setEnabled(
            False
        )

        self.senha_input.setEnabled(
            False
        )

        self.atualizar_texto_bloqueio()

        self.timer_bloqueio.start(
            1000
        )

    def atualizar_bloqueio(self):
        self.segundos_bloqueio -= 1

        if self.segundos_bloqueio <= 0:
            self.timer_bloqueio.stop()

            self.login_btn.setEnabled(
                True
            )

            self.usuario_input.setEnabled(
                True
            )

            self.senha_input.setEnabled(
                True
            )

            self.status_label.setText(
                "O acesso foi liberado. "
                "Tente novamente."
            )

            self.senha_input.clear()

            self.senha_input.setFocus()

            return

        self.atualizar_texto_bloqueio()

    def atualizar_texto_bloqueio(self):
        minutos = (
            self.segundos_bloqueio
            // 60
        )

        segundos = (
            self.segundos_bloqueio
            % 60
        )

        self.status_label.setText(
            (
                "Acesso temporariamente "
                "bloqueado.\n"
                f"Tente novamente em "
                f"{minutos:02d}:"
                f"{segundos:02d}."
            )
        )


# =========================================================
# ALTERAR SENHA
# =========================================================

class AlterarSenhaDialog(QDialog):

    def __init__(
        self,
        usuario_id,
        parent=None
    ):
        super().__init__(
            parent
        )

        self.usuario_id = (
            usuario_id
        )

        self.setWindowTitle(
            "Alterar senha"
        )

        self.setFixedSize(
            440,
            470
        )

        self.setModal(
            True
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            45,
            40,
            45,
            40
        )

        layout.setSpacing(
            14
        )

        titulo = QLabel(
            "Alterar senha"
        )

        titulo.setObjectName(
            "loginTitle"
        )

        descricao = QLabel(
            (
                "Confirme sua senha atual "
                "e defina uma nova senha."
            )
        )

        descricao.setObjectName(
            "loginDescription"
        )

        descricao.setWordWrap(
            True
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            descricao
        )

        layout.addSpacing(
            15
        )

        # =====================
        # SENHA ATUAL
        # =====================

        atual_label = QLabel(
            "SENHA ATUAL"
        )

        atual_label.setObjectName(
            "loginFieldLabel"
        )

        self.atual_input = (
            QLineEdit()
        )

        self.atual_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.atual_input.setPlaceholderText(
            "Digite sua senha atual"
        )

        self.atual_input.setMinimumHeight(
            44
        )

        layout.addWidget(
            atual_label
        )

        layout.addWidget(
            self.atual_input
        )

        # =====================
        # NOVA SENHA
        # =====================

        nova_label = QLabel(
            "NOVA SENHA"
        )

        nova_label.setObjectName(
            "loginFieldLabel"
        )

        self.nova_input = (
            QLineEdit()
        )

        self.nova_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.nova_input.setPlaceholderText(
            "8+ caracteres, letra e número"
        )

        self.nova_input.setMinimumHeight(
            44
        )

        layout.addWidget(
            nova_label
        )

        layout.addWidget(
            self.nova_input
        )

        # =====================
        # CONFIRMAR
        # =====================

        confirmar_label = QLabel(
            "CONFIRMAR NOVA SENHA"
        )

        confirmar_label.setObjectName(
            "loginFieldLabel"
        )

        self.confirmar_input = (
            QLineEdit()
        )

        self.confirmar_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.confirmar_input.setPlaceholderText(
            "Repita a nova senha"
        )

        self.confirmar_input.setMinimumHeight(
            44
        )

        layout.addWidget(
            confirmar_label
        )

        layout.addWidget(
            self.confirmar_input
        )

        layout.addStretch()

        self.salvar_btn = QPushButton(
            "Alterar senha"
        )

        self.salvar_btn.setObjectName(
            "loginButton"
        )

        self.salvar_btn.setMinimumHeight(
            46
        )

        layout.addWidget(
            self.salvar_btn
        )

        self.salvar_btn.clicked.connect(
            self.salvar
        )

        self.confirmar_input.returnPressed.connect(
            self.salvar
        )

        self.atual_input.setFocus()

    def salvar(self):
        senha_atual = (
            self.atual_input.text()
        )

        nova_senha = (
            self.nova_input.text()
        )

        confirmar = (
            self.confirmar_input.text()
        )

        if not (
            senha_atual
            and nova_senha
            and confirmar
        ):
            QMessageBox.warning(
                self,
                "Alterar senha",
                "Preencha todos os campos."
            )

            return

        if nova_senha != confirmar:

            QMessageBox.warning(
                self,
                "Senhas diferentes",
                (
                    "A nova senha "
                    "e a confirmação "
                    "não são iguais."
                )
            )

            return

        try:
            alterar_senha(
                self.usuario_id,
                senha_atual,
                nova_senha
            )

        except ValueError as erro:

            QMessageBox.warning(
                self,
                "Não foi possível alterar",
                str(erro)
            )

            return

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                (
                    "Não foi possível alterar "
                    "a senha.\n\n"
                    f"{erro}"
                )
            )

            return

        QMessageBox.information(
            self,
            "Senha alterada",
            (
                "Sua senha foi alterada "
                "com sucesso."
            )
        )

        self.accept()