import tkinter as tk
from tkinter import ttk, messagebox
import logging


class KanbanApp(tk.Tk):

    # ---------------- WINDOW VARIABLES ----------------

    BACKGROWND_COLOR: str = "#f0f0f0"
    DIMENSIONS = "600x500"
    START_AT_FULL_SCREEN = True
    TEXT_FONT = "Helvetica"

    # ---------------------------------------------------

    # ---------------- HEADER VARIABLES ----------------

    HEADER_TITLE_TEXT = "Kanban de Transparência"
    HEADER_TITLE_SIZE = 24
    HEADER_TITLE_STYLE = "bold"
    HEADER_TITLE_COLOR = "#333333"

    HEADER_SUBTITLE_TEXT = "Selecione o seu perfil de acesso"
    HEADER_SUBTITLE_SIZE = 12
    HEADER_SUBTITLE_COLOR = "#666666"

    # ---------------------------------------------------

    def __init__(self):

        super().__init__()

        self.title("Kanban de Transparência - Obras Públicas")
        self.geometry(self.DIMENSIONS)
        self.attributes("-zoomed", self.START_AT_FULL_SCREEN)
        self.configure(bg=self.BACKGROWND_COLOR)

        self.user_type = tk.StringVar(value="")

        self.create_widgets()

    def setUpHeader(self):
        header_frame = tk.Frame(self, bg=self.BACKGROWND_COLOR)
        header_frame.pack(pady=40)

        title_label = tk.Label(header_frame, text=self.HEADER_TITLE_TEXT,
                               font=(self.TEXT_FONT, self.HEADER_TITLE_SIZE,
                                     self.HEADER_TITLE_STYLE),
                               bg=self.BACKGROWND_COLOR, fg=self.HEADER_TITLE_COLOR)
        title_label.pack()

        subtitle_label = tk.Label(header_frame, text=self.HEADER_SUBTITLE_TEXT,
                                  font=(self.TEXT_FONT,
                                        self.HEADER_SUBTITLE_SIZE),
                                  bg=self.BACKGROWND_COLOR,
                                  fg=self.HEADER_SUBTITLE_COLOR)
        subtitle_label.pack(pady=5)

    def create_widgets(self):
        # --- Cabeçalho ---
        header_frame = tk.Frame(self, bg=self.BACKGROWND_COLOR)
        header_frame.pack(pady=40)

        title_label = tk.Label(
            header_frame,
            text="Kanban de Transparência",
            font=(self.TEXT_FONT, 24, "bold"),
            bg=self.BACKGROWND_COLOR,
            fg="#333333"
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Selecione o seu perfil de acesso",
            font=(self.TEXT_FONT, 12),
            bg=self.BACKGROWND_COLOR,
            fg="#666666"
        )
        subtitle_label.pack(pady=5)

        # --- Botões de Tipo de Usuário ---
        buttons_frame = tk.Frame(self, bg=self.BACKGROWND_COLOR)
        buttons_frame.pack(pady=20)

        # Estilo dos botões
        btn_config = {'width': 15, 'font': (
            self.TEXT_FONT, 10, "bold"), 'pady': 5}

        self.btn_civil = tk.Button(
            buttons_frame,
            text="CIVIL",
            command=lambda: self.setup_login_area("civil"),
            bg="#4CAF50", fg="white", **btn_config
        )
        self.btn_civil.grid(row=0, column=0, padx=10)

        self.btn_empresa = tk.Button(
            buttons_frame,
            text="EMPRESARIAL",
            command=lambda: self.setup_login_area("empresa"),
            bg="#2196F3", fg="white", **btn_config
        )
        self.btn_empresa.grid(row=0, column=1, padx=10)

        self.btn_gov = tk.Button(
            buttons_frame,
            text="GOVERNAMENTAL",
            command=lambda: self.setup_login_area("governo"),
            bg="#FF9800", fg="white", **btn_config
        )
        self.btn_gov.grid(row=0, column=2, padx=10)

        # --- Área Dinâmica de Login (Muda conforme o clique) ---
        self.login_area_frame = tk.Frame(
            self, bg="white", bd=1, relief="solid", padx=20, pady=20)
        self.login_area_frame.pack(pady=20, fill="x", padx=100)

        # Label inicial de instrução
        self.lbl_instruction = tk.Label(
            self.login_area_frame,
            text="Selecione uma opção acima para continuar.",
            bg="white", fg="#888"
        )
        self.lbl_instruction.pack()

    def setup_login_area(self, user_type):
        """Limpa a área de login e desenha os campos baseados no tipo de usuário"""
        self.user_type.set(user_type)

        # Limpar widgets anteriores da área de login
        for widget in self.login_area_frame.winfo_children():
            widget.destroy()

        # Título da seção de login
        role_titles = {
            "civil": "Acesso Cidadão",
            "empresa": "Acesso Corporativo",
            "governo": "Acesso Administrativo"
        }

        lbl_role = tk.Label(
            self.login_area_frame,
            text=role_titles.get(user_type),
            font=(self.TEXT_FONT, 14, "bold"),
            bg="white", fg="#333"
        )
        lbl_role.pack(pady=(0, 15))

        if user_type == "civil":
            # --- Fluxo CIVIL: Acesso direto ---
            lbl_info = tk.Label(
                self.login_area_frame,
                text="Visualize o andamento das obras públicas\nsem necessidade de cadastro.",
                bg="white", justify="center"
            )
            lbl_info.pack(pady=10)

            btn_enter = tk.Button(
                self.login_area_frame,
                text="ENTRAR NO SISTEMA",
                command=self.perform_login,
                bg="#4CAF50", fg="white", font=(self.TEXT_FONT, 11, "bold"), width=20
            )
            btn_enter.pack(pady=10)

        else:
            # --- Fluxo EMPRESA ou GOVERNO: Exige autenticação ---

            # Campo E-mail
            tk.Label(self.login_area_frame, text="E-mail:",
                     bg="white", anchor="w").pack(fill="x")
            self.entry_email = tk.Entry(self.login_area_frame)
            self.entry_email.pack(fill="x", pady=(0, 10))
            b = self.entry_email.get()
            logging.info(b)

            # Campo Senha
            tk.Label(self.login_area_frame, text="Senha:",
                     bg="white", anchor="w").pack(fill="x")
            self.entry_password = tk.Entry(self.login_area_frame, show="*")
            self.entry_password.pack(fill="x", pady=(0, 15))
            a = self.entry_password.get()
            logging.info(a)

            # Botão de Login
            btn_color = "#2196F3" if user_type == "empresa" else "#FF9800"
            btn_login = tk.Button(
                self.login_area_frame,
                text="AUTENTICAR",
                command=self.perform_login,
                bg=btn_color, fg="white", font=(self.TEXT_FONT, 11, "bold"), width=20
            )
            btn_login.pack(pady=5)

    def perform_login(self):
        """Simula a ação de entrar no sistema"""
        u_type = self.user_type.get()

        if u_type == "civil":
            messagebox.showinfo(
                "Sucesso", "Bem-vindo, Cidadão! Carregando Kanban público...")
            # Aqui chamaremos a tela do Kanban Civil futuramente

        else:
            # Validação simples para exemplo
            email = self.entry_email.get()
            senha = self.entry_password.get()

            if not email or not senha:
                messagebox.showwarning(
                    "Atenção", "Por favor, preencha e-mail e senha.")
                return

            # Simulação de verificação
            messagebox.showinfo(
                "Login", f"Tentando login como {u_type.upper()}...\nE-mail: {email}")
            # Aqui validaremos no banco de dados futuramente


if __name__ == "__main__":
    app = KanbanApp()
    app.mainloop()
