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

    # Botão Voltar
    BACK_BUTTON_TEXT = "< Voltar"
    BACK_BUTTON_BG = "#eee"
    BACK_BUTTON_BD = 0
    BACK_BUTTON_CURSOR = "hand2"

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

    ACTION_BTN_TEXT = "ABRIR KANBAN DA OBRA"
    ACTION_BTN_BG = "#4CAF50"
    ACTION_BTN_FG = "white"
    ACTION_BTN_FONT_STYLE = "bold"
    ACTION_BTN_FONT_SIZE = 9

    # endregion ---------------------------------------------------

    # region ---------------- LIST VARIABLES ----------------

    TREE_COLUMNS = ("Nome", "Local", "Status", "Data")
    
    # endregion ---------------------------------------------------

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

    def update_view(self, company_name, company_cnpj, company_email):
        """Método chamado ao entrar na tela"""
        self.company_name = company_name
        self.company_cnpj = company_cnpj
        self.company_email = company_email
        
        self.clearWidgets()
        self.createWidgets()
        self.load_data()

    def clearWidgets(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpFilters()
        self.setUpWorksList()

    def setUpHeader(self):
        header_frame = tk.Frame(self.content_frame, bg=self.HEADER_BG, 
                                bd=self.HEADER_BD, relief=self.HEADER_RELIEF, 
                                padx=self.HEADER_PAD, pady=self.HEADER_PAD)
        header_frame.pack(fill="x", pady=self.HEADER_PACK_PADY)

        # Barra Superior (Botão + Nome)
        top_bar = tk.Frame(header_frame, bg=self.HEADER_BG)
        top_bar.pack(fill="x", pady=(0, 10))
        
        # Botão Voltar
        def back_command(): return self.controller.show_frame("EmpresasCivilFrame")
        
        tk.Button(top_bar, text=self.BACK_BUTTON_TEXT, command=back_command,
                  bg=self.BACK_BUTTON_BG, bd=self.BACK_BUTTON_BD, 
                  cursor=self.BACK_BUTTON_CURSOR).pack(side="left")
        
        # Nome da Empresa
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

        tk.Label(filter_frame, text=self.SORT_LABEL_TEXT, bg=self.FILTER_FRAME_BG).pack(side="left")
        
        self.combo_sort = ttk.Combobox(filter_frame, values=self.COMBO_VALUES, 
                                       width=self.COMBO_WIDTH, state="readonly")
        self.combo_sort.current(0)
        self.combo_sort.pack(side="left", padx=5)

        tk.Button(filter_frame, text=self.APPLY_BTN_TEXT, command=self.apply_filter, 
                  bg=self.APPLY_BTN_BG, fg=self.APPLY_BTN_FG).pack(side="left", padx=10)
        
        # Botão de Ação Explícito
        tk.Button(filter_frame, text=self.ACTION_BTN_TEXT, command=self.open_kanban, 
                  bg=self.ACTION_BTN_BG, fg=self.ACTION_BTN_FG, 
                  font=(self.TEXT_FONT, self.ACTION_BTN_FONT_SIZE, self.ACTION_BTN_FONT_STYLE)).pack(side="right")

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
        sort_opt = self.combo_sort.get()
        data = self.works_data[:]
        
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
