import tkinter as tk
from tkinter import ttk, messagebox

from app.models.model_corporate_user import Corporate
from app.models.model_location import Location
from app.models.model_public_work import PublicWork


class ObrasEmpresaFrame(tk.Frame):

    # region ---------------- WINDOW VARIABLES ----------------
    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"
    # endregion

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)

        self.content_frame = tk.Frame(self, bg=self.WINDOW_BACKGROUND_COLOR)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Dados da tela
        self.company_name = ""
        self.company_cnpj = ""
        self.company_email = ""
        self.works_data = []

    def update_view(self, company_name=None, company_cnpj=None, company_email=None):
        # Limpa tela
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # --- LÓGICA CONDICIONAL ---
        if self.controller.user_type == "empresa":
            # Modo Empresa: Carrega dados do usuário logado (ignora args)
            my_id = self.controller.user_id
            data: Corporate = next((e for e in Corporate.listAll()
                                    if e.getId() == my_id), None)
            if data:
                self.company_name = data.getCompanyName()
                self.company_cnpj = data.getCnpj()
                self.company_email = data.getEmail()
        else:
            # Modo Civil: Usa dados passados pela tela anterior
            self.company_name = company_name
            self.company_cnpj = company_cnpj
            self.company_email = company_email

        self.createWidgets()
        self.load_data()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpFilters()
        self.setUpWorksList()

        # Botão Principal (Ação)
        btn_text = "GERENCIAR KANBAN DA OBRA" if self.controller.user_type == "empresa" else "VISUALIZAR KANBAN DA OBRA"
        btn_bg = "#4CAF50" if self.controller.user_type == "empresa" else "#2196F3"

        tk.Button(self.content_frame, text=btn_text, command=self.open_kanban,
                  bg=btn_bg, fg="white", font=("bold"), pady=10).pack(fill="x", pady=10)

    def setUpHeader(self):
        header_frame = tk.Frame(
            self.content_frame, bg="white", bd=1, relief="solid", padx=15, pady=15)
        header_frame.pack(fill="x", pady=(0, 20))

        top_bar = tk.Frame(header_frame, bg="white")
        top_bar.pack(fill="x", pady=(0, 10))

        # --- LÓGICA DE BOTÕES DO TOPO ---
        if self.controller.user_type == "empresa":
            # Empresa: Botão Sair à direita
            tk.Button(top_bar, text="Sair", command=lambda: self.controller.show_frame("LoginFrame"),
                      bg="#ff5252", fg="white", bd=0).pack(side="right")

            # Empresa: Botão Editar (AGORA FUNCIONAL)
            tk.Button(top_bar, text="Editar Dados da Empresa", bg="#ddd", bd=0, padx=10,
                      command=self.open_edit_modal).pack(side="right", padx=10)
        else:
            # Civil: Botão Voltar à esquerda
            tk.Button(top_bar, text="< Voltar", command=lambda: self.controller.show_frame("EmpresasCivilFrame"),
                      bg="#eee", bd=0).pack(side="left")

        # Título (Nome da Empresa)
        tk.Label(top_bar, text=self.company_name, font=("Helvetica", 16, "bold"),
                 bg="white", fg="#2196F3").pack(side="left", padx=15)

        # Info complementar
        info_text = f"CNPJ: {self.company_cnpj}    |    Contato: {self.company_email}"
        tk.Label(header_frame, text=info_text,
                 bg="white", fg="#555").pack(anchor="w")

    def setUpFilters(self):
        filter_frame = tk.Frame(
            self.content_frame, bg="#e0e0e0", padx=10, pady=10)
        filter_frame.pack(fill="x", pady=(0, 10))

        # 1. Ordenação (Para todos)
        tk.Label(filter_frame, text="Ordenar:", bg="#e0e0e0").pack(side="left")
        self.combo_sort = ttk.Combobox(filter_frame, values=[
                                       "A-Z", "Z-A", "Recentes", "Antigas"], width=15, state="readonly")
        self.combo_sort.current(0)
        self.combo_sort.pack(side="left", padx=5)
        tk.Button(filter_frame, text="Aplicar", command=self.apply_filter,
                  bg="#FF9800", fg="white").pack(side="left", padx=10)

        # 2. Pesquisa (Exibido para EMPRESA)
        if self.controller.user_type == "empresa":
            tk.Label(filter_frame, text="|  Pesquisar:",
                     bg="#e0e0e0").pack(side="left", padx=5)
            self.entry_search = tk.Entry(filter_frame, width=20)
            self.entry_search.pack(side="left", padx=5)
            tk.Button(filter_frame, text="Buscar", command=self.apply_filter,
                      bg="#2196F3", fg="white").pack(side="left")

    def setUpWorksList(self):
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill="both", expand=True)

        self.works_tree = ttk.Treeview(tree_frame, columns=(
            "Nome", "Local", "Status", "Data"), show="headings")
        self.works_tree.heading("Nome", text="Obra")
        self.works_tree.heading("Local", text="Local")
        self.works_tree.heading("Status", text="Status")
        self.works_tree.heading("Data", text="Início")

        self.works_tree.pack(fill="both", expand=True)
        self.works_tree.bind("<Double-1>", lambda e: self.open_kanban())

    def load_data(self):
        self.works_data: list[PublicWork] = PublicWork.listAll()
        self.populate_tree(self.works_data)

    def populate_tree(self, data: list[PublicWork]):
        for item in self.works_tree.get_children():
            self.works_tree.delete(item)
        for obra in data:
            local: Location = obra.getLocation()
            self.works_tree.insert("", "end", iid=obra.getId(), values=(
                obra.getTitle(), f"{local.getUf()} - {local.getCity()} - {local.getAddress()}", obra.getStatus(), obra.getStartDate().strftime("%d/%m/%Y")))

    def apply_filter(self):
        data = self.works_data[:]

        # Filtro de Busca
        if hasattr(self, 'entry_search'):
            term = self.entry_search.get().lower()
            if term:
                data = [x for x in data if term in x.getTitle().lower()]

        # Ordenação
        sort_opt = self.combo_sort.get()
        if sort_opt == "A-Z":
            data.sort(key=lambda x: x.getTitle())
        elif sort_opt == "Z-A":
            data.sort(key=lambda x: x.getTitle(), reverse=True)
        elif sort_opt == "Recentes":
            data.sort(key=lambda x: x.getStartDate(), reverse=True)
        elif sort_opt == "Antigas":
            data.sort(key=lambda x: x.getStartDate())

        self.populate_tree(data)

    def open_kanban(self):
        selected = self.works_tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma obra.")
            return

        work_id = selected[0]
        work_name = self.works_tree.item(work_id)['values'][0]
        self.controller.show_kanban_frame(work_id, work_name)

    def open_edit_modal(self):
        """ Abre janela modal para editar Nome, Email e Senha """
        modal = tk.Toplevel(self)
        modal.title("Editar Dados da Empresa")
        modal.geometry("400x350")
        modal.configure(bg="white")
        modal.grab_set()

        tk.Label(modal, text="Editar Meus Dados", font=(
            "Helvetica", 14, "bold"), bg="white", fg="#333").pack(pady=20)

        entries = {}

        def add_field(label, key, value, show=None):
            tk.Label(modal, text=label, font=("bold", 10), bg="white",
                     anchor="w").pack(fill="x", padx=40, pady=(5, 0))
            entry = tk.Entry(modal, bg="#fafafa", show=show)
            entry.insert(0, value)
            entry.pack(fill="x", padx=40, pady=(0, 10))
            entries[key] = entry

        # Campos
        add_field("Nome da Empresa:", "nome", self.company_name)
        add_field("E-mail de Contato:", "email", self.company_email)
        # Senha inicia vazia ou fictícia
        add_field("Nova Senha:", "senha", "", show="*")

        # Botão Salvar Mudanças
        tk.Button(modal, text="Salvar mudanças", bg="#4CAF50", fg="white", font=("bold"), pady=8,
                  command=lambda: self.confirm_update_popup(modal, entries)).pack(fill="x", padx=40, pady=20)

    def confirm_update_popup(self, parent_modal, entries):
        """ Popup de confirmação SIM/NÃO """
        popup = tk.Toplevel(self)
        popup.title("Confirmação")
        popup.geometry("350x150")
        popup.configure(bg="white")
        popup.grab_set()

        # Centraliza
        try:
            x = parent_modal.winfo_rootx() + 25
            y = parent_modal.winfo_rooty() + 100
            popup.geometry(f"+{x}+{y}")
        except:
            pass

        tk.Label(popup, text="Deseja salvar as alterações?",
                 font=("Helvetica", 12), bg="white").pack(pady=25)

        btn_frame = tk.Frame(popup, bg="white")
        btn_frame.pack()

        # Botão SIM (Verde, Esquerda)
        tk.Button(btn_frame, text="SIM", bg="#4CAF50", fg="white", width=10, font=("bold"),
                  command=lambda: self.save_company_data(parent_modal, popup, entries)).pack(side="left", padx=15)

        # Botão NÃO (Vermelho, Direita)
        tk.Button(btn_frame, text="NÃO", bg="#f44336", fg="white", width=10, font=("bold"),
                  command=popup.destroy).pack(side="right", padx=15)

    def save_company_data(self, modal, popup, entries):
        """ Atualiza o mock_db e a visualização """
        new_name = entries["nome"].get()
        new_email = entries["email"].get()
        # new_pass = entries["senha"].get() # Em um sistema real, salvaríamos a senha

        if not new_name or not new_email:
            messagebox.showwarning(
                "Erro", "Nome e E-mail são obrigatórios.", parent=popup)
            return

        corp: Corporate = Corporate.getById(self.controller.user_id)
        print(f"bah   {corp.getCompanyName()}   bah")

        if corp:
            corp.setCompanyName(new_name)
            corp.setEmail(new_email)
            corp.pushDatabase()

        # 2. Fechar janelas
        popup.destroy()
        modal.destroy()

        # 3. Recarregar a tela para refletir mudanças
        self.update_view()
        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
