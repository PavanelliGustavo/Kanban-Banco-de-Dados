import tkinter as tk
from tkinter import ttk, messagebox
import mock_db

class KanbanViewFrame(tk.Frame):

    # region ---------------- WINDOW VARIABLES ----------------

    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"
    TITLE_FONT = "Comic Sans MS"

    MAIN_CONTENT_PARAMS = {"bg": WINDOW_BACKGROUND_COLOR}
    MAIN_CONTENT_PACK_PARAMS = {"fill": "both", 
                                "expand": True, 
                                "padx": 20, 
                                "pady": 20}

    # endregion --------------------------------------------------

    # region ---------------- HEADER VARIABLES ----------------

    HEADER_FRAME_BG = "#f0f0f0"
    HEADER_FRAME_PACK_PADY = (0, 20)

    # Botão Voltar
    BACK_BUTTON_TEXT = "< Voltar"
    BACK_BUTTON_BG = "#ddd"
    BACK_BUTTON_PARAMS = {"bg": BACK_BUTTON_BG, "bd": 0}

    # Título da Obra
    WORK_TITLE_SIZE = 20
    WORK_TITLE_STYLE = "bold"
    WORK_TITLE_COLOR = "#333"
    WORK_TITLE_PARAMS = {"font": (TITLE_FONT, WORK_TITLE_SIZE, WORK_TITLE_STYLE),
                         "bg": HEADER_FRAME_BG,
                         "fg": WORK_TITLE_COLOR}

    # Botão Documentos
    DOCS_BUTTON_TEXT = "Acessar Documentos da Obra"
    DOCS_BUTTON_BG = "#607D8B"
    DOCS_BUTTON_FG = "white"
    DOCS_BUTTON_STYLE = "bold"
    DOCS_BUTTON_PARAMS = {"bg": DOCS_BUTTON_BG, 
                          "fg": DOCS_BUTTON_FG, 
                          "font": (TEXT_FONT, 10, DOCS_BUTTON_STYLE), 
                          "padx": 10}

    # endregion ---------------------------------------------------

    # region ---------------- KANBAN BOARD VARIABLES ----------------

    KANBAN_CONTAINER_BG = "#f0f0f0"
    
    COLUMNS_NAMES = ["Em Planejamento", "Em Andamento", "Em Verificação", "Concluído"]
    COLUMN_BG = "#e0e0e0"
    COLUMN_BD = 2
    COLUMN_RELIEF = "groove"
    COLUMN_TITLE_FONT_SIZE = 11
    COLUMN_TITLE_FONT_STYLE = "bold"
    COLUMN_TITLE_FG = "#555"
    
    CARD_BG = "white"
    CARD_BD = 1
    CARD_RELIEF = "raised"
    CARD_PADX = 10
    CARD_PADY = 5
    
    CARD_TITLE_SIZE = 10
    CARD_TITLE_STYLE = "bold"
    
    PREVISION_TEXT_SIZE = 8
    PREVISION_TEXT_FG = "#777"

    # endregion ---------------------------------------------------

    # region ---------------- MODAL VARIABLES ----------------

    MODAL_GEOMETRY = "400x500"
    MODAL_BG = "white"
    
    STATUS_COLORS = {
        "Concluído": "#4CAF50",
        "Em Andamento": "#2196F3",
        "DEFAULT": "#FFC107"
    }

    # endregion ---------------------------------------------------

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)
        
        self.main_content = tk.Frame(self, **self.MAIN_CONTENT_PARAMS)
        self.main_content.pack(**self.MAIN_CONTENT_PACK_PARAMS)
        
        self.current_work_id = None
        self.current_work_name = None

    def update_view(self, work_id, work_name):
        """Reconstrói o Kanban para a obra selecionada"""
        self.current_work_id = work_id
        self.current_work_name = work_name
        
        self.clearWidgets()
        self.createWidgets()

    def clearWidgets(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpKanbanBoard()

    def setUpHeader(self):
        header_frame = tk.Frame(self.main_content, bg=self.HEADER_FRAME_BG)
        header_frame.pack(fill="x", pady=self.HEADER_FRAME_PACK_PADY)

        # Botão Voltar
        def back_command():
            return self.controller.show_frame("EmpresasCivilFrame")

        tk.Button(header_frame, text=self.BACK_BUTTON_TEXT, command=back_command,
                  **self.BACK_BUTTON_PARAMS).pack(side="left")

        # Título da Obra (Centralizado)
        title_frame = tk.Frame(header_frame, bg=self.HEADER_FRAME_BG)
        title_frame.pack(side="left", expand=True, fill="x")
        
        tk.Label(title_frame, text=self.current_work_name, 
                 **self.WORK_TITLE_PARAMS).pack()

        # Botão Documentos
        tk.Button(header_frame, text=self.DOCS_BUTTON_TEXT, 
                  command=self.open_documents_page, 
                  **self.DOCS_BUTTON_PARAMS).pack(side="right")

    def setUpKanbanBoard(self):
        kanban_container = tk.Frame(self.main_content, bg=self.KANBAN_CONTAINER_BG)
        kanban_container.pack(fill="both", expand=True)
        
        # Filtrar tarefas
        tasks = [t for t in mock_db.KANBAN_TASKS_DB if t['obra_id'] == int(self.current_work_id)]

        for idx, col_name in enumerate(self.COLUMNS_NAMES):
            self.setUpColumn(kanban_container, idx, col_name, tasks)

    def setUpColumn(self, container, idx, col_name, all_tasks):
        # Frame da Coluna
        col_frame = tk.Frame(container, bg=self.COLUMN_BG, bd=self.COLUMN_BD, relief=self.COLUMN_RELIEF)
        container.grid_columnconfigure(idx, weight=1) 
        col_frame.grid(row=0, column=idx, sticky="nsew", padx=5, pady=5)

        # Título da Coluna
        tk.Label(col_frame, text=col_name, 
                 font=(self.TEXT_FONT, self.COLUMN_TITLE_FONT_SIZE, self.COLUMN_TITLE_FONT_STYLE), 
                 bg=self.COLUMN_BG, fg=self.COLUMN_TITLE_FG, pady=10).pack(fill="x")

        # Cards da Coluna
        col_tasks = [t for t in all_tasks if t['status'] == col_name]
        for task in col_tasks:
            self.createCard(col_frame, task)

    def createCard(self, parent_col, task_data):
        card = tk.Frame(parent_col, bg=self.CARD_BG, bd=self.CARD_BD, relief=self.CARD_RELIEF, 
                        padx=self.CARD_PADX, pady=self.CARD_PADY)
        card.pack(fill="x", padx=self.CARD_PADX, pady=5)
        
        lbl_title = tk.Label(card, text=task_data['titulo'], 
                             font=(self.TEXT_FONT, self.CARD_TITLE_SIZE, self.CARD_TITLE_STYLE), 
                             bg=self.CARD_BG, wraplength=150, justify="left")
        lbl_title.pack(anchor="w")

        if task_data.get('previsao'):
            tk.Label(card, text=f"Prev: {task_data['previsao']}", 
                     font=(self.TEXT_FONT, self.PREVISION_TEXT_SIZE), 
                     fg=self.PREVISION_TEXT_FG, bg=self.CARD_BG).pack(anchor="w", pady=(5,0))

        # Bindings e Cursor
        def open_modal(e): return self.showCardModal(task_data)
        
        card.bind("<Button-1>", open_modal)
        lbl_title.bind("<Button-1>", open_modal)
        
        card.configure(cursor="hand2")
        lbl_title.configure(cursor="hand2")

    def showCardModal(self, task):
        modal = tk.Toplevel(self)
        modal.title(f"Detalhes: {task['titulo']}")
        modal.geometry(self.MODAL_GEOMETRY)
        modal.configure(bg=self.MODAL_BG)
        
        # Garante compatibilidade Linux
        modal.wait_visibility() 
        modal.transient(self) 
        modal.grab_set()

        # Conteúdo do Modal
        self.setUpModalContent(modal, task)

    def setUpModalContent(self, modal, task):
        # Título
        tk.Label(modal, text=task['titulo'], 
                 font=(self.TEXT_FONT, 16, "bold"), 
                 bg=self.MODAL_BG, fg="#2196F3", wraplength=380).pack(pady=(20, 10))
        
        # Badge de Status
        status_color = self.STATUS_COLORS.get(task['status'], self.STATUS_COLORS["DEFAULT"])
        
        tk.Label(modal, text=task['status'].upper(), 
                 font=(self.TEXT_FONT, 9, "bold"), 
                 bg=status_color, fg="white", padx=10, pady=2).pack(pady=(0, 20))

        # Grid de Informações
        info_frame = tk.Frame(modal, bg=self.MODAL_BG, padx=20)
        info_frame.pack(fill="x")

        self.addModalDetail(info_frame, "Responsável:", task.get('responsavel', 'Não informado'))
        self.addModalDetail(info_frame, "Previsão/Status:", task.get('previsao', '-'))
        
        # Divisor
        ttk.Separator(modal, orient='horizontal').pack(fill='x', padx=20, pady=15)

        # Descrição
        tk.Label(modal, text="Descrição da Atividade:", 
                 font=(self.TEXT_FONT, 11, "bold"), bg=self.MODAL_BG, anchor="w").pack(fill="x", padx=20)
        
        desc_frame = tk.Frame(modal, bg="#f9f9f9", bd=1, relief="solid")
        desc_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        tk.Label(desc_frame, text=task.get('descricao_completa', 'Sem descrição detalhada.'), 
                 bg="#f9f9f9", wraplength=340, justify="left", padx=10, pady=10).pack(fill="both", expand=True, anchor="nw")

        # Botão Fechar
        tk.Button(modal, text="Fechar", command=modal.destroy, bg="#ddd", width=10).pack(pady=15)

    def addModalDetail(self, parent, label, value):
        row = tk.Frame(parent, bg=self.MODAL_BG)
        row.pack(fill="x", pady=5)
        tk.Label(row, text=label, font=(self.TEXT_FONT, 10, "bold"), 
                 bg=self.MODAL_BG, width=15, anchor="w").pack(side="left")
        tk.Label(row, text=value, font=(self.TEXT_FONT, 10), 
                 bg=self.MODAL_BG, anchor="w", wraplength=230, justify="left").pack(side="left", fill="x")

    def open_documents_page(self):
        self.controller.show_docs_frame(self.current_work_id, self.current_work_name)
