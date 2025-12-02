import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re

# Models Reais
from app.models.model_card import Card
from app.models.model_column import Column
from app.models.model_public_work import PublicWork
from app.models.model_corporate_user import Corporate

class KanbanViewFrame(tk.Frame):

    # region ---------------- WINDOW VARIABLES ----------------
    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"
    
    MAIN_CONTENT_BG = "#f0f0f0"
    MAIN_CONTENT_PARAMS = {"fill": "both", "expand": True, "padx": 20, "pady": 20}
    # endregion

    # region ---------------- HEADER VARIABLES ----------------
    HEADER_BG = "#f0f0f0"
    HEADER_PADY = (0, 20)

    BACK_BTN_TEXT = "< Voltar"
    BACK_BTN_BG = "#ddd"
    
    TITLE_FONT = ("Comic Sans MS", 18, "bold")
    TITLE_FG = "#333"

    ACTION_BTN_DOCS_BG = "#607D8B"
    ACTION_BTN_ADD_BG = "#2196F3"
    ACTION_BTN_COL_BG = "#9C27B0"
    ACTION_BTN_FG = "white"
    ACTION_BTN_FONT = ("bold")
    # endregion

    # region ---------------- KANBAN BOARD VARIABLES ----------------
    BOARD_BG = "#f0f0f0"
    
    COL_BG = "#e0e0e0"
    COL_WIDTH = 260
    COL_TITLE_FONT = (TEXT_FONT, 11, "bold")
    COL_TITLE_FG = "#555"
    
    CARD_BG = "white"
    CARD_TITLE_FONT = (TEXT_FONT, 10, "bold")
    CARD_FG = "#333"
    CARD_PREV_FG = "#777"
    # endregion

    # region ---------------- MODAL VARIABLES ----------------
    MODAL_BG = "white"
    MODAL_TITLE_FONT = (TEXT_FONT, 14, "bold")
    MODAL_BTN_SAVE_BG = "#4CAF50"
    MODAL_BTN_EDIT_BG = "#FF9800"
    MODAL_BTN_DEL_BG = "#f44336"
    MODAL_BTN_FG = "white"
    # endregion

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)
        
        self.main_content = tk.Frame(self, bg=self.MAIN_CONTENT_BG)
        self.main_content.pack(**self.MAIN_CONTENT_PARAMS)
        
        self.current_work_id = None
        self.current_work_name = None

    def update_view(self, work_id, work_name):
        self.current_work_id = int(work_id)
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
        header_frame = tk.Frame(self.main_content, bg=self.HEADER_BG)
        header_frame.pack(fill="x", pady=self.HEADER_PADY)

        # Lado Esquerdo (Voltar + Título)
        left_frame = tk.Frame(header_frame, bg=self.HEADER_BG)
        left_frame.pack(side="left", fill="y")

        tk.Button(left_frame, text=self.BACK_BTN_TEXT, command=self.goBack,
                  bg=self.BACK_BTN_BG, bd=0, padx=10).pack(side="left")

        user_type = getattr(self.controller, 'user_type', 'civil')
        title_prefix = "Gerenciamento: " if user_type == "empresa" else ""
        
        tk.Label(left_frame, text=f"{title_prefix}{self.current_work_name}",
                 font=self.TITLE_FONT, bg=self.HEADER_BG, fg=self.TITLE_FG).pack(side="left", padx=20)

        # Lado Direito (Ações)
        right_frame = tk.Frame(header_frame, bg=self.HEADER_BG)
        right_frame.pack(side="right")

        # Botão Documentos (Para todos)
        tk.Button(right_frame, text="Documentos da Obra",
                  command=self.open_docs, 
                  bg=self.ACTION_BTN_DOCS_BG, fg=self.ACTION_BTN_FG, 
                  font=self.ACTION_BTN_FONT, width=20, pady=5).pack(side="top", pady=(0, 5))

        # Ações exclusivas de Empresa
        if user_type == "empresa":
            tk.Button(right_frame, text="+ Adicionar Card",
                      command=self.open_create_card_modal, 
                      bg=self.ACTION_BTN_ADD_BG, fg=self.ACTION_BTN_FG, 
                      font=self.ACTION_BTN_FONT, width=20, pady=2).pack(side="top", pady=2)

            tk.Button(right_frame, text="+ Adicionar Coluna",
                      command=lambda: self.open_column_modal(None, True), 
                      bg=self.ACTION_BTN_COL_BG, fg=self.ACTION_BTN_FG, 
                      font=self.ACTION_BTN_FONT, width=20, pady=2).pack(side="top", pady=2)

    def setUpKanbanBoard(self):
        container = tk.Frame(self.main_content, bg=self.BOARD_BG)
        container.pack(fill="both", expand=True)

        # --- CANVAS & SCROLLBAR ---
        canvas = tk.Canvas(container, bg=self.BOARD_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        
        scrollable_frame = tk.Frame(canvas, bg=self.BOARD_BG)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Ajusta altura do frame interno para acompanhar o canvas
        def configure_canvas_height(event):
            canvas.itemconfig(canvas_window, height=event.height)
        canvas.bind("<Configure>", configure_canvas_height)

        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")

        # --- CARREGAMENTO DE DADOS (DB) ---
        # 1. Colunas
        # Filtra colunas desta obra específica
        all_cols = Column.listAll()
        columns_data = [c for c in all_cols if c.getPublicWorkId() == self.current_work_id]
        columns_data.sort(key=lambda x: int(x.getPosition()))

        # 2. Cards
        all_cards = Card.listAll()
        tasks = [t for t in all_cards if t.getPublicWorkId() == self.current_work_id]
        tasks.sort(key=lambda x: int(x.getPosition()))

        # --- RENDERIZAÇÃO ---
        for col_data in columns_data:
            self.createColumn(scrollable_frame, col_data, tasks)

    def createColumn(self, parent, col_data: Column, all_tasks: list[Card]):
        col_id = col_data.getId()
        col_name = col_data.getName()
        col_pos = col_data.getPosition()

        col_frame = tk.Frame(parent, bg=self.COL_BG, bd=2, relief="groove", width=self.COL_WIDTH)
        col_frame.pack(side="left", fill="y", padx=5, pady=5)
        col_frame.pack_propagate(False) # Mantém largura fixa

        # Cabeçalho da Coluna
        header_text = f"{col_pos}. {col_name}"
        header_lbl = tk.Label(col_frame, text=header_text, font=self.COL_TITLE_FONT, 
                              bg=self.COL_BG, fg=self.COL_TITLE_FG, pady=10)
        header_lbl.pack(fill="x")

        # Se for empresa, permite clicar para editar a coluna
        if getattr(self.controller, 'user_type', 'civil') == "empresa":
            header_lbl.bind("<Button-1>", lambda e, c=col_data: self.open_column_modal(c, False))
            header_lbl.configure(cursor="hand2")

        # Cards da Coluna
        col_tasks = [t for t in all_tasks if t.getColumnId() == col_id]
        for task in col_tasks:
            self.createCard(col_frame, task)

    def createCard(self, parent, task: Card):
        card = tk.Frame(parent, bg=self.CARD_BG, bd=1, relief="raised", padx=10, pady=10)
        card.pack(fill="x", padx=10, pady=5)

        pos = task.getPosition()
        display_text = f"{pos}. {task.getTitle()}"

        lbl = tk.Label(card, text=display_text, font=self.CARD_TITLE_FONT, 
                       bg=self.CARD_BG, fg=self.CARD_FG, wraplength=230, justify="left")
        lbl.pack(anchor="w")
        
        # Exibir prazo se houver
        deadline = task.getDeadline()
        if deadline:
            d_str = deadline.strftime("%d/%m/%Y")
            tk.Label(card, text=f"Prev: {d_str}", font=(self.TEXT_FONT, 8), 
                     bg=self.CARD_BG, fg=self.CARD_PREV_FG).pack(anchor="w")

        # Ação de clique
        def open_modal(e): return self.showCardModal(task)
        card.bind("<Button-1>", open_modal)
        lbl.bind("<Button-1>", open_modal)
        card.configure(cursor="hand2")

    # region ---------------- MODALS (DETAILS / EDIT) ----------------

    def showCardModal(self, task: Card):
        modal = tk.Toplevel(self)
        modal.title(f"Detalhes: {task.getTitle()}")
        modal.geometry("400x550")
        modal.configure(bg=self.MODAL_BG)
        modal.grab_set()

        pos = task.getPosition()
        tk.Label(modal, text=f"{pos}. {task.getTitle()}", font=("Helvetica", 16, "bold"), 
                 bg=self.MODAL_BG, fg="#2196F3", wraplength=380).pack(pady=20)

        info = tk.Frame(modal, bg=self.MODAL_BG, padx=20)
        info.pack(fill="x")

        # Busca o prazo formatado
        deadline_str = task.getDeadline().strftime("%d/%m/%Y") if task.getDeadline() else "-"

        details = [
            ("ID Coluna:", task.getColumnId()),
            ("Prazo:", deadline_str),
            ("Posição:", str(task.getPosition()))
        ]

        for k, v in details:
            row = tk.Frame(info, bg=self.MODAL_BG)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=k, font=("bold", 10), bg=self.MODAL_BG, width=12, anchor="w").pack(side="left")
            tk.Label(row, text=v, bg=self.MODAL_BG, anchor="w").pack(side="left")

        tk.Label(modal, text="Descrição:", font=("bold", 10), bg=self.MODAL_BG, anchor="w").pack(fill="x", padx=20, pady=(15, 0))
        
        desc = tk.Label(modal, text=task.getDescription(), bg="#f9f9f9", 
                        wraplength=360, justify="left", relief="solid", bd=1)
        desc.pack(fill="both", expand=True, padx=20, pady=5)

        # Botões de Ação (Apenas Empresa)
        if getattr(self.controller, 'user_type', 'civil') == "empresa":
            btn_frame = tk.Frame(modal, bg=self.MODAL_BG)
            btn_frame.pack(fill="x", pady=20, padx=20)

            tk.Button(btn_frame, text="EDITAR", bg=self.MODAL_BTN_EDIT_BG, fg=self.MODAL_BTN_FG, font=("bold"),
                      command=lambda: [modal.destroy(), self.open_edit_form(task, False)]).pack(side="left", fill="x", expand=True, padx=5)

            tk.Button(btn_frame, text="EXCLUIR", bg=self.MODAL_BTN_DEL_BG, fg=self.MODAL_BTN_FG, font=("bold"),
                      command=lambda: self.confirm_popup(modal, "delete", task)).pack(side="left", fill="x", expand=True, padx=5)

    def open_create_card_modal(self):
        self.open_edit_form(None, True)

    def open_edit_form(self, task_data: Card | None, is_new):
        modal = tk.Toplevel(self)
        title = "Novo Card" if is_new else "Editar Card"
        modal.title(title)
        modal.geometry("400x650")
        modal.configure(bg=self.MODAL_BG)
        modal.grab_set()

        tk.Label(modal, text=title, font=self.MODAL_TITLE_FONT, bg=self.MODAL_BG).pack(pady=15)

        entries = {}
        
        # Busca colunas disponíveis para o combobox
        all_cols = Column.listAll()
        available_cols = [c for c in all_cols if c.getPublicWorkId() == self.current_work_id]
        available_cols.sort(key=lambda x: x.getPosition())
        col_ids = [c.getId() for c in available_cols]

        # Helpers para preencher campos
        val_t = "" if is_new else task_data.getTitle()
        val_c = str(col_ids[0]) if (is_new and col_ids) else str(task_data.getColumnId() if task_data else "")
        
        val_p = ""
        if not is_new and task_data.getDeadline():
            val_p = task_data.getDeadline().strftime("%d/%m/%Y")
            
        val_pos = "" if is_new else str(task_data.getPosition())
        val_d = "" if is_new else task_data.getDescription()

        def add_field(label, key, val, kind="entry", opts=None):
            tk.Label(modal, text=label, bg=self.MODAL_BG, anchor="w").pack(fill="x", padx=30, pady=(5, 0))
            if kind == "entry":
                e = tk.Entry(modal, bg="#fafafa")
                e.insert(0, val)
                e.pack(fill="x", padx=30)
                entries[key] = e
            elif kind == "combo":
                e = ttk.Combobox(modal, values=opts, state="readonly")
                e.set(val)
                e.pack(fill="x", padx=30)
                entries[key] = e
            elif kind == "text":
                e = tk.Text(modal, height=5, bg="#fafafa")
                e.insert("1.0", val)
                e.pack(fill="x", padx=30)
                entries[key] = e

        add_field("Título", "titulo", val_t)
        add_field("Posição", "posicao", val_pos)
        add_field("Coluna ID (Selecionar)", "status", val_c, "combo", col_ids)
        add_field("Prazo (dd/mm/aaaa)", "previsao", val_p)
        add_field("Descrição", "descricao", val_d, "text")

        tk.Button(modal, text="SALVAR", bg=self.MODAL_BTN_SAVE_BG, fg=self.MODAL_BTN_FG, font=("bold"), pady=10,
                  command=lambda: self.confirm_popup(modal, "save", task_data, entries, is_new)).pack(fill="x", padx=30, pady=30)

    def open_column_modal(self, col_data: Column, is_new):
        modal = tk.Toplevel(self)
        title_text = "Adicionar Coluna" if is_new else "Editar Coluna"
        modal.title(title_text)
        modal.geometry("350x350")
        modal.configure(bg=self.MODAL_BG)
        modal.grab_set()

        tk.Label(modal, text=title_text, font=self.MODAL_TITLE_FONT, bg=self.MODAL_BG, fg=self.ACTION_BTN_COL_BG).pack(pady=20)

        entries = {}
        val_title = "" if is_new else col_data.getName()
        val_pos = "" if is_new else str(col_data.getPosition())

        tk.Label(modal, text="Título da Coluna:", bg=self.MODAL_BG, anchor="w").pack(fill="x", padx=30, pady=(5, 0))
        e_t = tk.Entry(modal, bg="#fafafa")
        e_t.insert(0, val_title)
        e_t.pack(fill="x", padx=30)
        entries['titulo'] = e_t

        tk.Label(modal, text="Posição:", bg=self.MODAL_BG, anchor="w").pack(fill="x", padx=30, pady=(15, 0))
        e_p = tk.Entry(modal, bg="#fafafa")
        e_p.insert(0, val_pos)
        e_p.pack(fill="x", padx=30)
        entries['posicao'] = e_p

        if is_new:
            tk.Button(modal, text="Salvar", bg=self.MODAL_BTN_SAVE_BG, fg="white", font=("bold"), pady=8, width=20,
                      command=lambda: self.save_column_action(modal, entries, col_data, True)).pack(pady=30)
        else:
            btn_frame = tk.Frame(modal, bg=self.MODAL_BG)
            btn_frame.pack(fill="x", pady=30, padx=30)
            tk.Button(btn_frame, text="EDITAR", bg=self.MODAL_BTN_EDIT_BG, fg="white", font=("bold"),
                      command=lambda: self.save_column_action(modal, entries, col_data, False)).pack(side="left", fill="x", expand=True, padx=5)
            tk.Button(btn_frame, text="EXCLUIR", bg=self.MODAL_BTN_DEL_BG, fg="white", font=("bold"),
                      command=lambda: self.confirm_popup(modal, "delete_col", col_data)).pack(side="left", fill="x", expand=True, padx=5)

    # endregion

    # region ---------------- ACTIONS (SAVE/DELETE) ----------------

    def save_column_action(self, modal, entries, col_data, is_new):
        title = entries['titulo'].get().strip()
        pos = entries['posicao'].get().strip()

        if not title or not pos.isdigit():
            messagebox.showwarning("Erro", "Título e Posição (número) são obrigatórios.", parent=modal)
            return

        if is_new:
            # Cria nova coluna (Model) e salva
            new_col = Column(title, int(pos), self.current_work_id)
            new_col.pushDatabase()
        else:
            col_data.setName(title)
            col_data.setPosition(int(pos))
            col_data.pushDatabase()

        modal.destroy()
        self.update_view(self.current_work_id, self.current_work_name)
        messagebox.showinfo("Sucesso", "Coluna salva!")

    def confirm_popup(self, parent_modal, action, data_obj=None, entries=None, is_new=False):
        """Gerencia todas as confirmações e salvamentos complexos (Cards)"""
        
        if action == "delete_col":
            if messagebox.askyesno("Confirmar", "Excluir coluna e seus cards?", parent=parent_modal):
                data_obj.delete() # Chama método do Model
                parent_modal.destroy()
                self.update_view(self.current_work_id, self.current_work_name)
            return

        if action == "delete": # Card
            if messagebox.askyesno("Confirmar", "Excluir card?", parent=parent_modal):
                data_obj.delete()
                parent_modal.destroy()
                self.update_view(self.current_work_id, self.current_work_name)
            return

        if action == "save": # Card
            t = entries['titulo'].get().strip()
            col_id_str = entries['status'].get().strip()
            p_str = entries['previsao'].get().strip()
            pos_str = entries['posicao'].get().strip()
            d = entries['descricao'].get("1.0", "end-1c").strip()

            if not t or not col_id_str or not p_str or not pos_str:
                messagebox.showwarning("Erro", "Preencha Título, Coluna, Prazo e Posição.", parent=parent_modal)
                return

            try:
                # Conversão de Data fundamental para o Banco
                date_obj = datetime.strptime(p_str, "%d/%m/%Y").date()
                pos_int = int(pos_str)
                col_int = int(col_id_str)
            except ValueError:
                messagebox.showwarning("Erro", "Data inválida (use dd/mm/aaaa) ou números inválidos.", parent=parent_modal)
                return

            if is_new:
                # Cria Card
                new_card = Card(t, d, pos_int, date_obj, col_int, self.current_work_id)
                new_card.pushDatabase()
            else:
                # Atualiza Card existente
                data_obj.setTitle(t)
                data_obj.setDescription(d)
                data_obj.setPosition(pos_int)
                data_obj.setDeadline(date_obj)
                data_obj.setColumnId(col_int)
                data_obj.pushDatabase()

            parent_modal.destroy()
            self.update_view(self.current_work_id, self.current_work_name)
            messagebox.showinfo("Sucesso", "Card salvo!")

    # endregion

    # region ---------------- NAVIGATION ----------------
    def goBack(self):
        user_type = getattr(self.controller, 'user_type', 'civil')
        if user_type == "empresa":
            self.controller.show_obras_frame()
        else:
            # Lógica para voltar para a lista correta
            try:
                # Tenta achar a empresa dona da obra para re-renderizar a tela anterior
                all_works = PublicWork.listAll()
                obra = next((o for o in all_works if o.getId() == self.current_work_id), None)
                if obra:
                    corp_id = obra.getCorporateId()
                    self.controller.show_obras_frame(corporate_id=corp_id)
                else:
                    self.controller.show_frame("EmpresasCivilFrame")
            except:
                self.controller.show_frame("EmpresasCivilFrame")

    def open_docs(self):
        self.controller.show_docs_frame(self.current_work_id, self.current_work_name)
    # endregion
