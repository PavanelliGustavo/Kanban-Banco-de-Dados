import tkinter as tk
from tkinter import ttk, messagebox
import mock_db

class ObrasEmpresaFrame(tk.Frame):

    # region ---------------- WINDOW VARIABLES ----------------

    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"
    
    CONTENT_FRAME_BG = "#f0f0f0"
    CONTENT_FRAME_PARAMS = {"fill": "both", 
                            "expand": True, 
                            "padx": 20, 
                            "pady": 20}

    # endregion --------------------------------------------------

    # region ---------------- HEADER VARIABLES ----------------

    HEADER_BG = "white"
    HEADER_BD = 1
    HEADER_RELIEF = "solid"
    HEADER_PAD = 15
    HEADER_PACK_PADY = (0, 20)

    # Botão Voltar (Civil)
    BACK_BUTTON_TEXT = "< Voltar"
    BACK_BUTTON_BG = "#eee"
    BACK_BUTTON_BD = 0
    BACK_BUTTON_CURSOR = "hand2"

    # Botão Sair (Empresa)
    LOGOUT_BUTTON_TEXT = "Sair"
    LOGOUT_BUTTON_BG = "#ff5252"
    LOGOUT_BUTTON_FG = "white"
    
    # Botão Editar (Empresa)
    EDIT_BUTTON_TEXT = "Editar Dados da Empresa"
    EDIT_BUTTON_BG = "#ddd"
    EDIT_BUTTON_BD = 0

    # Título da Empresa
    COMPANY_NAME_FONT_SIZE = 16
    COMPANY_NAME_FONT_STYLE = "bold"
    COMPANY_NAME_FG = "#2196F3"
    
    # Informações (CNPJ/Email)
    INFO_FG = "#555"

    # endregion ---------------------------------------------------

    # region ---------------- FILTER VARIABLES ----------------

    FILTER_FRAME_BG = "#e0e0e0"
    FILTER_FRAME_PAD = 10
    FILTER_FRAME_PACK_PADY = (0, 10)

    SORT_LABEL_TEXT = "Ordenar:"
    COMBO_VALUES = ["A-Z", "Z-A", "Recentes", "Antigas"]
    COMBO_WIDTH = 15

    APPLY_BTN_TEXT = "Aplicar"
    APPLY_BTN_BG = "#FF9800"
    APPLY_BTN_FG = "white"

    # Pesquisa (Empresa)
    SEARCH_LABEL_TEXT = "|  Pesquisar:"
    SEARCH_BTN_TEXT = "Buscar"
    SEARCH_BTN_BG = "#2196F3"
    SEARCH_BTN_FG = "white"

    # Botão Ação Principal (Visualizar/Gerenciar)
    ACTION_BTN_BG_CIVIL = "#2196F3" # Azul
    ACTION_BTN_BG_CORP = "#4CAF50"  # Verde
    ACTION_BTN_FG = "white"
    ACTION_BTN_FONT_STYLE = "bold"

    # endregion ---------------------------------------------------

    # region ---------------- LIST VARIABLES ----------------

    TREE_COLUMNS = ("Nome", "Local", "Status", "Data")
    
    # endregion ---------------------------------------------------

    # region ---------------- MODAL VARIABLES ----------------
    
    MODAL_BG = "white"
    MODAL_TITLE_FONT = (TEXT_FONT, 14, "bold")
    
    MODAL_BTN_SAVE_BG = "#4CAF50"
    MODAL_BTN_SAVE_FG = "white"
    
    POPUP_CONFIRM_BG = "white"
    
    # endregion

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)
        
        self.content_frame = tk.Frame(self, bg=self.CONTENT_FRAME_BG)
        self.content_frame.pack(**self.CONTENT_FRAME_PARAMS)

        # Variáveis de Estado
        self.company_name = ""
        self.company_cnpj = ""
        self.company_email = ""
        self.works_data = []

    def update_view(self, company_name=None, company_cnpj=None, company_email=None):
        """Método chamado ao entrar na tela"""
        self.clearWidgets()
        
        # Lógica de Dados: Define de onde vêm as informações
        # IMPORTANTE: Seu controller (App) precisa ter user_type e user_id definidos
        current_user_type = getattr(self.controller, 'user_type', 'civil')
        
        if current_user_type == "empresa":
            # Busca dados do banco baseado no ID do usuário logado
            my_id = getattr(self.controller, 'user_id', 1) # Fallback para 1 se não houver ID
            data = next((e for e in mock_db.EMPRESAS_DB if e["id"] == int(my_id)), None)
            
            if data:
                self.company_name = data["nome"]
                self.company_cnpj = data["cnpj"]
                self.company_email = data["email"]
            else:
                self.company_name = "Empresa não encontrada"
        else:
            # Usa os dados passados por argumento (Fluxo Civil)
            self.company_name = company_name
            self.company_cnpj = company_cnpj
            self.company_email = company_email

        self.createWidgets()
        self.load_data()

    def clearWidgets(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpFilters()
        self.setUpWorksList()
        self.setUpMainActionButton()

    def setUpHeader(self):
        header_frame = tk.Frame(self.content_frame, bg=self.HEADER_BG, 
                                bd=self.HEADER_BD, relief=self.HEADER_RELIEF, 
                                padx=self.HEADER_PAD, pady=self.HEADER_PAD)
        header_frame.pack(fill="x", pady=self.HEADER_PACK_PADY)

        # Barra Superior (Botões e Título)
        top_bar = tk.Frame(header_frame, bg=self.HEADER_BG)
        top_bar.pack(fill="x", pady=(0, 10))
        
        user_type = getattr(self.controller, 'user_type', 'civil')

        if user_type == "empresa":
            # --- HEADER EMPRESA ---
            # Nome na esquerda
            tk.Label(top_bar, text=self.company_name, 
                     font=(self.TEXT_FONT, self.COMPANY_NAME_FONT_SIZE, self.COMPANY_NAME_FONT_STYLE), 
                     bg=self.HEADER_BG, fg=self.COMPANY_NAME_FG).pack(side="left")
            
            # Botões na direita
            tk.Button(top_bar, text=self.LOGOUT_BUTTON_TEXT, 
                      command=lambda: self.controller.show_frame("LoginFrame"),
                      bg=self.LOGOUT_BUTTON_BG, fg=self.LOGOUT_BUTTON_FG, bd=0).pack(side="right")
            
            tk.Button(top_bar, text=self.EDIT_BUTTON_TEXT, 
                      command=self.open_edit_modal,
                      bg=self.EDIT_BUTTON_BG, bd=self.EDIT_BUTTON_BD, padx=10).pack(side="right", padx=10)

        else:
            # --- HEADER CIVIL ---
            # Botão Voltar na esquerda
            def back_command(): return self.controller.show_frame("EmpresasCivilFrame")
            tk.Button(top_bar, text=self.BACK_BUTTON_TEXT, command=back_command,
                      bg=self.BACK_BUTTON_BG, bd=self.BACK_BUTTON_BD, 
                      cursor=self.BACK_BUTTON_CURSOR).pack(side="left")
            
            # Nome
            tk.Label(top_bar, text=self.company_name, 
                     font=(self.TEXT_FONT, self.COMPANY_NAME_FONT_SIZE, self.COMPANY_NAME_FONT_STYLE), 
                     bg=self.HEADER_BG, fg=self.COMPANY_NAME_FG).pack(side="left", padx=15)

        # Grid de Informações
        info_grid = tk.Frame(header_frame, bg=self.HEADER_BG)
        info_grid.pack(fill="x")
        
        info_text = f"CNPJ: {self.company_cnpj}    |    Contato: {self.company_email}"
        tk.Label(info_grid, text=info_text, bg=self.HEADER_BG, fg=self.INFO_FG).pack(anchor="w")

    def setUpFilters(self):
        filter_frame = tk.Frame(self.content_frame, bg=self.FILTER_FRAME_BG, 
                                padx=self.FILTER_FRAME_PAD, pady=self.FILTER_FRAME_PAD)
        filter_frame.pack(fill="x", pady=self.FILTER_FRAME_PACK_PADY)

        # 1. Ordenação (Comum a todos)
        tk.Label(filter_frame, text=self.SORT_LABEL_TEXT, bg=self.FILTER_FRAME_BG).pack(side="left")
        
        self.combo_sort = ttk.Combobox(filter_frame, values=self.COMBO_VALUES, 
                                       width=self.COMBO_WIDTH, state="readonly")
        self.combo_sort.current(0)
        self.combo_sort.pack(side="left", padx=5)

        tk.Button(filter_frame, text=self.APPLY_BTN_TEXT, command=self.apply_filter, 
                  bg=self.APPLY_BTN_BG, fg=self.APPLY_BTN_FG).pack(side="left", padx=10)
        
        # 2. Pesquisa (Exclusivo Empresa)
        user_type = getattr(self.controller, 'user_type', 'civil')
        if user_type == "empresa":
            tk.Label(filter_frame, text=self.SEARCH_LABEL_TEXT, bg=self.FILTER_FRAME_BG).pack(side="left", padx=5)
            self.entry_search = tk.Entry(filter_frame, width=20)
            self.entry_search.pack(side="left", padx=5)
            tk.Button(filter_frame, text=self.SEARCH_BTN_TEXT, command=self.apply_filter, 
                      bg=self.SEARCH_BTN_BG, fg=self.SEARCH_BTN_FG).pack(side="left")

    def setUpWorksList(self):
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill="both", expand=True)

        self.works_tree = ttk.Treeview(tree_frame, columns=self.TREE_COLUMNS, show="headings")
        
        self.works_tree.heading("Nome", text="Obra")
        self.works_tree.heading("Local", text="Local")
        self.works_tree.heading("Status", text="Status")
        self.works_tree.heading("Data", text="Início")
        
        self.works_tree.pack(fill="both", expand=True)

        # Binding de Duplo Clique
        self.works_tree.bind("<Double-1>", lambda e: self.open_kanban())

    def setUpMainActionButton(self):
        user_type = getattr(self.controller, 'user_type', 'civil')
        
        btn_text = "GERENCIAR KANBAN DA OBRA" if user_type == "empresa" else "VISUALIZAR KANBAN DA OBRA"
        btn_bg = self.ACTION_BTN_BG_CORP if user_type == "empresa" else self.ACTION_BTN_BG_CIVIL
        
        tk.Button(self.content_frame, text=btn_text, command=self.open_kanban, 
                  bg=btn_bg, fg=self.ACTION_BTN_FG, 
                  font=(self.TEXT_FONT, 10, self.ACTION_BTN_FONT_STYLE), pady=10).pack(fill="x", pady=10)

    # region ---------------- DATA LOADING & LOGIC ----------------

    def load_data(self):
        self.works_data = [obra for obra in mock_db.OBRAS_DB if obra['empresa'] == self.company_name]
        self.populate_tree(self.works_data)

    def populate_tree(self, data):
        for item in self.works_tree.get_children():
            self.works_tree.delete(item)
        for obra in data:
            self.works_tree.insert("", "end", iid=obra['id'], 
                                   values=(obra['nome'], obra['local'], obra['status'], obra['data_inicio']))

    def apply_filter(self):
        data = self.works_data[:]
        
        # Filtro de Busca (Se existir o widget)
        if hasattr(self, 'entry_search'):
            term = self.entry_search.get().lower()
            if term:
                data = [x for x in data if term in x['nome'].lower() or term in x['local'].lower()]

        sort_opt = self.combo_sort.get()
        
        if sort_opt == "A-Z":
            data.sort(key=lambda x: x['nome'])
        elif sort_opt == "Z-A":
            data.sort(key=lambda x: x['nome'], reverse=True)
        elif sort_opt == "Recentes":
            data.sort(key=lambda x: x['data_inicio'], reverse=True)
        elif sort_opt == "Antigas":
            data.sort(key=lambda x: x['data_inicio'])
            
        self.populate_tree(data)

    def open_kanban(self):
        selected = self.works_tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma obra para visualizar o Kanban.")
            return

        work_id = selected[0]
        work_name = self.works_tree.item(work_id)['values'][0]

        self.controller.show_kanban_frame(work_id, work_name)

    # endregion

    # region ---------------- EDIT MODAL LOGIC ----------------

    def open_edit_modal(self):
        """ Abre janela modal para editar Nome, Email e Senha """
        modal = tk.Toplevel(self)
        modal.title("Editar Dados da Empresa")
        modal.geometry("400x350")
        modal.configure(bg=self.MODAL_BG)
        
        # Compatibilidade Linux
        modal.wait_visibility()
        modal.grab_set()

        tk.Label(modal, text="Editar Meus Dados", font=self.MODAL_TITLE_FONT, 
                 bg=self.MODAL_BG, fg="#333").pack(pady=20)

        entries = {}
        
        def add_field(label, key, value, show=None):
            tk.Label(modal, text=label, font=("bold", 10), bg=self.MODAL_BG, anchor="w").pack(fill="x", padx=40, pady=(5, 0))
            entry = tk.Entry(modal, bg="#fafafa", show=show)
            entry.insert(0, value)
            entry.pack(fill="x", padx=40, pady=(0, 10))
            entries[key] = entry

        # Campos
        add_field("Nome da Empresa:", "nome", self.company_name)
        add_field("E-mail de Contato:", "email", self.company_email)
        add_field("Nova Senha:", "senha", "", show="*")

        # Botão Salvar
        tk.Button(modal, text="Salvar mudanças", 
                  bg=self.MODAL_BTN_SAVE_BG, fg=self.MODAL_BTN_SAVE_FG, font=("bold"), pady=8,
                  command=lambda: self.confirm_update_popup(modal, entries)).pack(fill="x", padx=40, pady=20)

    def confirm_update_popup(self, parent_modal, entries):
        """ Popup de confirmação SIM/NÃO """
        popup = tk.Toplevel(self)
        popup.title("Confirmação")
        popup.geometry("350x150")
        popup.configure(bg=self.POPUP_CONFIRM_BG)
        
        popup.wait_visibility()
        popup.grab_set()
        
        # Tenta centralizar
        try:
            x = parent_modal.winfo_rootx() + 25
            y = parent_modal.winfo_rooty() + 100
            popup.geometry(f"+{x}+{y}")
        except: pass

        tk.Label(popup, text="Deseja salvar as alterações?", font=("Helvetica", 12), bg=self.POPUP_CONFIRM_BG).pack(pady=25)

        btn_frame = tk.Frame(popup, bg=self.POPUP_CONFIRM_BG)
        btn_frame.pack()

        tk.Button(btn_frame, text="SIM", bg="#4CAF50", fg="white", width=10, font=("bold"),
                  command=lambda: self.save_company_data(parent_modal, popup, entries)).pack(side="left", padx=15)

        tk.Button(btn_frame, text="NÃO", bg="#f44336", fg="white", width=10, font=("bold"),
                  command=popup.destroy).pack(side="right", padx=15)

    def save_company_data(self, modal, popup, entries):
        new_name = entries["nome"].get()
        new_email = entries["email"].get()
        # new_pass = entries["senha"].get()

        if not new_name or not new_email:
            messagebox.showwarning("Erro", "Nome e E-mail são obrigatórios.", parent=popup)
            return

        # Atualizar no Banco de Dados Mockado
        user_id = getattr(self.controller, 'user_id', None)
        empresa = next((e for e in mock_db.EMPRESAS_DB if e["id"] == int(user_id if user_id else 0)), None)
        
        if empresa:
            empresa["nome"] = new_name
            empresa["email"] = new_email
        
        popup.destroy()
        modal.destroy()

        self.update_view() 
        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")

    # endregion
