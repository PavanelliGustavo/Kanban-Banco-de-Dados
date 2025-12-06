import tkinter as tk
from tkinter import messagebox
from app.models.model_corporate_user import Corporate
from app.models.model_government_user import Government  

class LoginFrame(tk.Frame):

    # region ---------------- ESTILOS ----------------
    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"
    # endregion

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)

        self.selected_profile = tk.StringVar(value="")
        self.createWidgets()

    def createWidgets(self):
        # Cabeçalho
        tk.Label(self, text="Kanban de Transparência", font=(
            "Helvetica", 24, "bold"), bg="#f0f0f0", fg="#333").pack(pady=40)
        tk.Label(self, text="Selecione o seu perfil de acesso", font=(
            "Helvetica", 12), bg="#f0f0f0", fg="#666").pack(pady=5)

        # Botões de Seleção de Perfil
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        def select(profile):
            self.selected_profile.set(profile)
            self.update_login_area(profile)

        # Botões Coloridos
        tk.Button(btn_frame, text="CIVIL", command=lambda: select("civil"), bg="#4CAF50",
                  fg="white", width=15, font=("bold"), pady=5).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="EMPRESA", command=lambda: select("empresa"), bg="#2196F3",
                  fg="white", width=15, font=("bold"), pady=5).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="GOVERNO", command=lambda: select("governo"), bg="#FF9800",
                  fg="white", width=15, font=("bold"), pady=5).grid(row=0, column=2, padx=10)

        # Área de Login (Muda conforme seleção)
        self.login_area = tk.Frame(
            self, bg="white", bd=1, relief="solid", padx=40, pady=30)
        self.login_area.pack(pady=20, fill="x", padx=150)

        # Texto inicial
        tk.Label(self.login_area, text="Selecione uma opção acima para continuar.",
                 bg="white", fg="#888").pack()

    def update_login_area(self, profile):
        # Limpa área de login
        for widget in self.login_area.winfo_children():
            widget.destroy()

        titles = {
            "civil": "Acesso Cidadão",
            "empresa": "Acesso Corporativo",
            "governo": "Acesso Administrativo"
        }

        tk.Label(self.login_area, text=titles[profile], font=(
            "Helvetica", 14, "bold"), bg="white", fg="#333").pack(pady=(0, 15))

        if profile == "civil":
            tk.Label(self.login_area, text="Visualize obras e gastos públicos sem senha.",
                     bg="white").pack(pady=10)
            tk.Button(self.login_area, text="ENTRAR NO SISTEMA", command=self.performLogin,
                      bg="#4CAF50", fg="white", font=("bold"), width=25, pady=5).pack(pady=10)
        else:
            # Campos de Email/Senha para Empresa e Governo
            tk.Label(self.login_area, text="E-mail:",
                     bg="white", anchor="w").pack(fill="x")
            self.entry_email = tk.Entry(self.login_area)
            self.entry_email.pack(fill="x", pady=(0, 10))

            tk.Label(self.login_area, text="Senha:",
                     bg="white", anchor="w").pack(fill="x")
            self.entry_pass = tk.Entry(self.login_area, show="*")
            self.entry_pass.pack(fill="x", pady=(0, 15))

            color = "#2196F3" if profile == "empresa" else "#FF9800"
            tk.Button(self.login_area, text="AUTENTICAR", command=self.performLogin,
                      bg=color, fg="white", font=("bold"), width=25, pady=5).pack(pady=5)

    def performLogin(self):
        profile = self.selected_profile.get()

        # 1. Fluxo CIVIL
        if profile == "civil":
            self.controller.user_type = "civil"
            self.controller.show_frame("EmpresasCivilFrame")

        # 2. Fluxo EMPRESA
        elif profile == "empresa":
            self.authenticate_corporate()

        # 3. Fluxo GOVERNO
        elif profile == "governo":
            self.authenticate_government()

    def authenticate_corporate(self):
        email = self.entry_email.get()
        password = self.entry_pass.get()

        if not email or not password:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        try:
            corporates: list[Corporate] = Corporate.listAll()
            corporate_match = next(
                (corp for corp in corporates if corp.getEmail() == email), None)

            if not corporate_match or not corporate_match.checkPassword(password):
                messagebox.showwarning("Erro", "Credenciais de Empresa inválidas.")
                return

            self.controller.user_type = "empresa"
            self.controller.user_id = corporate_match.getId()

            self.controller.show_obras_frame(
                nome=corporate_match.getCompanyName(),
                cnpj=corporate_match.getCnpj(),
                email=corporate_match.getEmail()
            )
        except Exception as e:
             messagebox.showerror("Erro", f"Erro ao conectar com banco: {e}")

    def authenticate_government(self):
        email = self.entry_email.get()
        password = self.entry_pass.get()

        if not email or not password:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        try:
            # Tenta buscar a lista de governos do Banco de Dados
            # Se der erro aqui, certifique-se que o método listAll() existe no model_government_user.py
            governments: list[Government] = Government.listAll()
            
            gov_match = next((gov for gov in governments if gov.getEmail() == email), None)

            if not gov_match or not gov_match.checkPassword(password):
                messagebox.showwarning("Erro", "Credenciais do Governo inválidas.")
                return

            # Login Sucesso
            self.controller.user_type = "governo"
            self.controller.user_id = gov_match.getId() 

            self.controller.show_frame("GovCentralViewFrame")
            
        except Exception as e:
            # Se cair aqui e o erro for 'listAll', verifique seu model
            messagebox.showerror("Erro Crítico", f"Falha ao conectar com tabela Government: {e}")
            