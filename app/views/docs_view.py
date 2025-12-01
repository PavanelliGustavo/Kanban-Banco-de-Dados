import tkinter as tk
from tkinter import ttk, messagebox
import mock_db

class DocsViewFrame(tk.Frame):

    # region ---------------- WINDOW VARIABLES ----------------

    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"
    
    MAIN_CONTENT_PADDING = 40
    MAIN_CONTENT_PARAMS = {"bg": WINDOW_BACKGROUND_COLOR}
    MAIN_CONTENT_PACK_PARAMS = {"fill": "both", 
                                "expand": True, 
                                "padx": MAIN_CONTENT_PADDING, 
                                "pady": MAIN_CONTENT_PADDING}

    # endregion --------------------------------------------------

    # region ---------------- HEADER VARIABLES ----------------

    HEADER_FRAME_BG = "#f0f0f0"
    HEADER_FRAME_PACK_PADY = (0, 20)

    # Botão Voltar
    BACK_BUTTON_TEXT = "< Voltar para o Kanban"
    BACK_BUTTON_BG = "#ddd"
    BACK_BUTTON_FG = "black"
    BACK_BUTTON_PARAMS = {"bg": BACK_BUTTON_BG, 
                          "bd": 0, 
                          "padx": 10, 
                          "pady": 5}
    
    # Título Principal
    TITLE_TEXT = "Documentos"
    TITLE_FONT_SIZE = 24
    TITLE_FONT_STYLE = "bold"
    TITLE_COLOR = "#333"
    TITLE_PARAMS = {"font": (TEXT_FONT, TITLE_FONT_SIZE, TITLE_FONT_STYLE),
                    "bg": HEADER_FRAME_BG,
                    "fg": TITLE_COLOR}
    
    # Subtítulo (Referente a...)
    SUBTITLE_FONT_SIZE = 10
    SUBTITLE_FONT_STYLE = "italic"
    SUBTITLE_COLOR = "#666"
    SUBTITLE_PARAMS = {"font": (TEXT_FONT, SUBTITLE_FONT_SIZE, SUBTITLE_FONT_STYLE),
                       "bg": HEADER_FRAME_BG,
                       "fg": SUBTITLE_COLOR}

    # endregion ---------------------------------------------------

    # region ---------------- FILTER AREA VARIABLES ----------------

    FILTER_FRAME_BG = "#e0e0e0"
    FILTER_FRAME_PAD = 10
    FILTER_FRAME_PACK_PADY = (0, 10)

    FILTER_LABEL_TEXT = "Ordenar arquivos por:"
    FILTER_LABEL_PARAMS = {"bg": FILTER_FRAME_BG}

    COMBOBOX_WIDTH = 20
    COMBOBOX_VALUES = ["A-Z (Nome)", "Z-A (Nome)", "Mais Recentes", "Mais Antigos"]
    
    APPLY_BUTTON_TEXT = "Aplicar Ordem"
    APPLY_BUTTON_BG = "#FF9800"
    APPLY_BUTTON_FG = "white"
    APPLY_BUTTON_PARAMS = {"bg": APPLY_BUTTON_BG, 
                           "fg": APPLY_BUTTON_FG}

    # endregion ---------------------------------------------------

    # region ---------------- LIST AREA VARIABLES ----------------

    TREE_COLUMNS = ("Documento", "Tipo", "Data")
    TREE_HEIGHT = 10
    
    COL_DOCUMENTO_WIDTH = 400
    COL_TIPO_WIDTH = 100
    COL_DATA_WIDTH = 150

    # endregion ---------------------------------------------------

    # region ---------------- ACTION BUTTON VARIABLES ----------------

    ACTION_BUTTON_TEXT = "ABRIR DOCUMENTO SELECIONADO"
    ACTION_BUTTON_BG = "#607D8B"
    ACTION_BUTTON_FG = "white"
    ACTION_BUTTON_FONT_STYLE = "bold"
    ACTION_BUTTON_PARAMS = {"bg": ACTION_BUTTON_BG, 
                            "fg": ACTION_BUTTON_FG, 
                            "font": (TEXT_FONT, 10, ACTION_BUTTON_FONT_STYLE),
                            "pady": 10}
    ACTION_BUTTON_PACK_PADY = 20

    # endregion ---------------------------------------------------

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)
        
        self.main_content = tk.Frame(self, **self.MAIN_CONTENT_PARAMS)
        self.main_content.pack(**self.MAIN_CONTENT_PACK_PARAMS)
        
        self.current_work_id = None
        self.current_work_name = None
        self.current_docs = [] 

    def update_view(self, work_id, work_name):
        self.current_work_id = work_id
        self.current_work_name = work_name
        
        self.clearWidgets()
        self.createWidgets()
        self.loadInitialData()

    def clearWidgets(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpFilterArea()
        self.setUpDocumentList()
        self.setUpActionButton()

    def setUpHeader(self):
        header_frame = tk.Frame(self.main_content, bg=self.HEADER_FRAME_BG)
        header_frame.pack(fill="x", pady=self.HEADER_FRAME_PACK_PADY)

        # Botão Voltar
        def back_command(): 
            return self.controller.show_kanban_frame(self.current_work_id, self.current_work_name)

        tk.Button(header_frame, text=self.BACK_BUTTON_TEXT, command=back_command,
                  **self.BACK_BUTTON_PARAMS).pack(side="left")
        
        # Título
        tk.Label(header_frame, text=self.TITLE_TEXT, 
                 **self.TITLE_PARAMS).pack(side="left", padx=30)
        
        # Subtítulo Dinâmico
        subtitle_text = f"Referente a: {self.current_work_name}"
        tk.Label(header_frame, text=subtitle_text, 
                 **self.SUBTITLE_PARAMS).pack(side="bottom", anchor="w")

    def setUpFilterArea(self):
        filter_frame = tk.Frame(self.main_content, bg=self.FILTER_FRAME_BG, 
                                padx=self.FILTER_FRAME_PAD, pady=self.FILTER_FRAME_PAD)
        filter_frame.pack(fill="x", pady=self.FILTER_FRAME_PACK_PADY)

        tk.Label(filter_frame, text=self.FILTER_LABEL_TEXT, 
                 **self.FILTER_LABEL_PARAMS).pack(side="left")
        
        self.combo_sort = ttk.Combobox(filter_frame, values=self.COMBOBOX_VALUES, 
                                       width=self.COMBOBOX_WIDTH, state="readonly")
        self.combo_sort.current(2) # Padrão: Mais Recentes
        self.combo_sort.pack(side="left", padx=5)

        tk.Button(filter_frame, text=self.APPLY_BUTTON_TEXT, command=self.apply_sort, 
                  **self.APPLY_BUTTON_PARAMS).pack(side="left", padx=10)

    def setUpDocumentList(self):
        tree_frame = tk.Frame(self.main_content)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=self.TREE_COLUMNS, show="headings", height=self.TREE_HEIGHT)
        
        # Configuração das Colunas
        self.tree.heading("Documento", text="Nome do Arquivo")
        self.tree.heading("Tipo", text="Formato")
        self.tree.heading("Data", text="Data de Publicação")
        
        self.tree.column("Documento", width=self.COL_DOCUMENTO_WIDTH)
        self.tree.column("Tipo", width=self.COL_TIPO_WIDTH, anchor="center")
        self.tree.column("Data", width=self.COL_DATA_WIDTH, anchor="center")

        self.tree.pack(fill="both", expand=True, side="left")
        
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)
        
        # Bind duplo clique
        self.tree.bind("<Double-1>", self.on_open_document)

    def setUpActionButton(self):
        tk.Button(self.main_content, text=self.ACTION_BUTTON_TEXT, 
                  command=self.on_open_document, 
                  **self.ACTION_BUTTON_PARAMS).pack(fill="x", pady=self.ACTION_BUTTON_PACK_PADY)

    def loadInitialData(self):
        if hasattr(mock_db, 'DOCUMENTS_DB'):
            self.current_docs = [d for d in mock_db.DOCUMENTS_DB if d['obra_id'] == int(self.current_work_id)]
        else:
            self.current_docs = []
        
        # Aplica a ordenação inicial (Mais Recentes)
        self.apply_sort()

    def populate_tree(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not data:
            self.tree.insert("", "end", values=("Nenhum documento encontrado.", "-", "-"))
        else:
            for doc in data:
                self.tree.insert("", "end", iid=doc['id'], values=(doc['titulo'], doc['tipo'], doc['data']))

    def apply_sort(self):
        sort_opt = self.combo_sort.get()
        
        if sort_opt == "A-Z (Nome)":
            self.current_docs.sort(key=lambda x: x['titulo'])
        elif sort_opt == "Z-A (Nome)":
            self.current_docs.sort(key=lambda x: x['titulo'], reverse=True)
        elif sort_opt == "Mais Recentes":
            self.current_docs.sort(key=lambda x: x['data'], reverse=True)
        elif sort_opt == "Mais Antigos":
            self.current_docs.sort(key=lambda x: x['data'])
            
        self.populate_tree(self.current_docs)

    def on_open_document(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um documento para visualizar.")
            return
            
        item_values = self.tree.item(selected[0])['values']
        if item_values[1] == "-": 
            return

        doc_name = item_values[0]
        messagebox.showinfo("Visualização de Documento", f"O sistema abriria o arquivo:\n\n{doc_name}\n\n(Funcionalidade simulada)")
