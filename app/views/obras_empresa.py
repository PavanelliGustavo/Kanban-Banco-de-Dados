import tkinter as tk
from tkinter import ttk, messagebox
import mock_db

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

    def update_view(self, company_name, company_cnpj, company_email):
        # Limpa tela
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # --- LÓGICA CONDICIONAL ---
        if self.controller.user_type == "empresa":
            # Modo Empresa: Carrega dados do usuário logado (ignora args)
            my_id = self.controller.user_id
            data = next((e for e in mock_db.EMPRESAS_DB if e["id"] == my_id), None)
            if data:
                self.company_name = data["nome"]
                self.company_cnpj = data["cnpj"]
                self.company_email = data["email"]
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
        header_frame = tk.Frame(self.content_frame, bg="white", bd=1, relief="solid", padx=15, pady=15)
        header_frame.pack(fill="x", pady=(0, 20))

        top_bar = tk.Frame(header_frame, bg="white")
        top_bar.pack(fill="x", pady=(0, 10))
        
        # --- LÓGICA DE BOTÕES DO TOPO ---
        if self.controller.user_type == "empresa":
            # Empresa: Botão Sair à direita
            tk.Button(top_bar, text="Sair", command=lambda: self.controller.show_frame("LoginFrame"),
                      bg="#ff5252", fg="white", bd=0).pack(side="right")
            
            # Empresa: Botão Editar
            tk.Button(top_bar, text="Editar Dados da Empresa", bg="#ddd", bd=0, padx=10,
                      command=lambda: messagebox.showinfo("Editar", "Funcionalidade de edição cadastral.")).pack(side="right", padx=10)
        else:
            # Civil: Botão Voltar à esquerda
            tk.Button(top_bar, text="< Voltar", command=lambda: self.controller.show_frame("EmpresasCivilFrame"),
                      bg="#eee", bd=0).pack(side="left")
        
        # Título (Nome da Empresa)
        tk.Label(top_bar, text=self.company_name, font=("Helvetica", 16, "bold"), 
                 bg="white", fg="#2196F3").pack(side="left", padx=15)

        # Info complementar
        info_text = f"CNPJ: {self.company_cnpj}    |    Contato: {self.company_email}"
        tk.Label(header_frame, text=info_text, bg="white", fg="#555").pack(anchor="w")

    def setUpFilters(self):
        filter_frame = tk.Frame(self.content_frame, bg="#e0e0e0", padx=10, pady=10)
        filter_frame.pack(fill="x", pady=(0, 10))

        # 1. Ordenação (Para todos)
        tk.Label(filter_frame, text="Ordenar:", bg="#e0e0e0").pack(side="left")
        self.combo_sort = ttk.Combobox(filter_frame, values=["A-Z", "Z-A", "Recentes", "Antigas"], width=15, state="readonly")
        self.combo_sort.current(0)
        self.combo_sort.pack(side="left", padx=5)
        tk.Button(filter_frame, text="Aplicar", command=self.apply_filter, bg="#FF9800", fg="white").pack(side="left", padx=10)
        
        # 2. Pesquisa (Exibido para EMPRESA, conforme pedido)
        if self.controller.user_type == "empresa":
            tk.Label(filter_frame, text="|  Pesquisar:", bg="#e0e0e0").pack(side="left", padx=5)
            self.entry_search = tk.Entry(filter_frame, width=20)
            self.entry_search.pack(side="left", padx=5)
            tk.Button(filter_frame, text="Buscar", command=self.apply_filter, bg="#2196F3", fg="white").pack(side="left")

    def setUpWorksList(self):
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill="both", expand=True)

        self.works_tree = ttk.Treeview(tree_frame, columns=("Nome", "Local", "Status", "Data"), show="headings")
        self.works_tree.heading("Nome", text="Obra")
        self.works_tree.heading("Local", text="Local")
        self.works_tree.heading("Status", text="Status")
        self.works_tree.heading("Data", text="Início")
        
        self.works_tree.pack(fill="both", expand=True)
        self.works_tree.bind("<Double-1>", lambda e: self.open_kanban())

    def load_data(self):
        # Carrega obras apenas desta empresa
        self.works_data = [obra for obra in mock_db.OBRAS_DB if obra['empresa'] == self.company_name]
        self.populate_tree(self.works_data)

    def populate_tree(self, data):
        for item in self.works_tree.get_children():
            self.works_tree.delete(item)
        for obra in data:
            self.works_tree.insert("", "end", iid=obra['id'], values=(obra['nome'], obra['local'], obra['status'], obra['data_inicio']))

    def apply_filter(self):
        data = self.works_data[:]
        
        # Filtro de Busca (Se existir o widget)
        if hasattr(self, 'entry_search'):
            term = self.entry_search.get().lower()
            if term:
                data = [x for x in data if term in x['nome'].lower() or term in x['local'].lower()]

        # Ordenação
        sort_opt = self.combo_sort.get()
        if sort_opt == "A-Z": data.sort(key=lambda x: x['nome'])
        elif sort_opt == "Z-A": data.sort(key=lambda x: x['nome'], reverse=True)
        elif sort_opt == "Recentes": data.sort(key=lambda x: x['data_inicio'], reverse=True)
        elif sort_opt == "Antigas": data.sort(key=lambda x: x['data_inicio'])
            
        self.populate_tree(data)

    def open_kanban(self):
        selected = self.works_tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma obra.")
            return

        work_id = selected[0]
        work_name = self.works_tree.item(work_id)['values'][0]
        self.controller.show_kanban_frame(work_id, work_name)
