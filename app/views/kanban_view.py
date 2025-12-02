from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import re

from app.models.model_card import Card
from app.models.model_column import Column
from app.models.model_corporate_user import Corporate
from app.models.model_public_work import PublicWork


class KanbanViewFrame(tk.Frame):

    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)

        self.main_content = tk.Frame(self, bg=self.WINDOW_BACKGROUND_COLOR)
        self.main_content.pack(fill="both", expand=True, padx=20, pady=20)

        self.current_work_id = None
        self.current_work_name = None

    def update_view(self, work_id, work_name):
        self.current_work_id = int(work_id)
        self.current_work_name = work_name

        for widget in self.main_content.winfo_children():
            widget.destroy()

        self.createWidgets()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpKanbanBoard()

    def setUpHeader(self):
        header_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        header_frame.pack(fill="x", pady=(0, 20))

        left_frame = tk.Frame(header_frame, bg="#f0f0f0")
        left_frame.pack(side="left", fill="y")

        def back():
            if self.controller.user_type == "empresa":
                self.controller.show_obras_frame()
            else:
                obra: PublicWork = next(
                    (o for o in PublicWork.listAll() if o.getId() == self.current_work_id), None)
                if obra:
                    emp: Corporate = next(
                        (e for e in Corporate.listAll() if e.getId() == obra.getCorporateId()), None)
                    if emp:
                        self.controller.show_obras_frame(
                            emp.getCompanyName(), emp.getCnpj(), emp.getEmail())
                    else:
                        self.controller.show_frame("EmpresasCivilFrame")

        tk.Button(left_frame, text="< Voltar", command=back,
                  bg="#ddd", bd=0, padx=10).pack(side="left")

        title_prefix = "Gerenciamento: " if self.controller.user_type == "empresa" else ""
        tk.Label(left_frame, text=f"{title_prefix}{self.current_work_name}",
                 font=("Comic Sans MS", 18, "bold"), bg="#f0f0f0", fg="#333").pack(side="left", padx=20)

        right_frame = tk.Frame(header_frame, bg="#f0f0f0")
        right_frame.pack(side="right")

        if self.controller.user_type == "empresa":
            tk.Button(right_frame, text="Acessar Documentos da Obra",
                      command=self.open_docs, bg="#607D8B", fg="white", font=("bold"), width=25, pady=5).pack(side="top", pady=(0, 5))

            tk.Button(right_frame, text="Adicionar Card",
                      command=self.open_create_card_modal, bg="#2196F3", fg="white", font=("bold"), width=25, pady=5).pack(side="top", pady=2)

            tk.Button(right_frame, text="Adicionar Coluna",
                      command=lambda: self.open_column_modal(None, True), bg="#9C27B0", fg="white", font=("bold"), width=25, pady=5).pack(side="top", pady=2)

        else:
            tk.Button(right_frame, text="Documentos da Obra",
                      command=self.open_docs, bg="#607D8B", fg="white", padx=10).pack()

    def setUpKanbanBoard(self):
        container = tk.Frame(self.main_content, bg="#f0f0f0")
        container.pack(fill="both", expand=True)

        # --- CANVAS & SCROLLBAR ---
        canvas = tk.Canvas(container, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            container, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw")

        def configure_canvas_height(event):
            canvas.itemconfig(canvas_window, height=event.height)
        canvas.bind("<Configure>", configure_canvas_height)

        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")

        # --- DADOS ---
        columns_data: list[Column] = [c for c in Column.listAll()
                                      if c.getPublicWorkId() == self.current_work_id]
        if not columns_data:
            columns_data = []
        columns_data.sort(key=lambda x: int(x.getPosition()))

        tasks: list[Card] = [t for t in Card.listAll()
                             if t.getPublicWorkId() == self.current_work_id]

        tasks.sort(key=lambda x: int(x.getPosition()))

        for idx, col_data in enumerate(columns_data):
            col_id = col_data.getId()
            col_name = col_data.getName()
            col_pos_visual = col_data.getPosition()

            col_frame = tk.Frame(scrollable_frame, bg="#e0e0e0",
                                 bd=2, relief="groove", width=260)
            col_frame.pack(side="left", fill="y", padx=5, pady=5)
            col_frame.pack_propagate(False)

            # Cabeçalho da Coluna (Clicável para Empresa)
            header_text = f"{col_pos_visual}. {col_name}"
            header_lbl = tk.Label(col_frame, text=header_text, font=(
                "Helvetica", 11, "bold"), bg="#e0e0e0", fg="#555", pady=10)
            header_lbl.pack(fill="x")

            if self.controller.user_type == "empresa":
                header_lbl.bind("<Button-1>", lambda e,
                                c=col_data: self.open_column_modal(c, False))
                header_lbl.configure(cursor="hand2")

            # Cards
            col_tasks = [t for t in tasks if t.getId() == col_id]
            for task in col_tasks:
                self.createCard(col_frame, task)

    def createCard(self, parent, task: Card):
        card = tk.Frame(parent, bg="white", bd=1,
                        relief="raised", padx=10, pady=10)
        card.pack(fill="x", padx=10, pady=5)

        pos = task.getPosition()
        display_text = f"{pos}. {task.getTitle()}"

        lbl = tk.Label(card, text=display_text, font=(
            "Helvetica", 10, "bold"), bg="white", wraplength=230, justify="left")
        lbl.pack(anchor="w")

        def cmd(e): return self.showCardModal(task)
        card.bind("<Button-1>", cmd)
        lbl.bind("<Button-1>", cmd)
        card.configure(cursor="hand2")

    def showCardModal(self, task: Card):
        modal = tk.Toplevel(self)
        modal.title(f"Detalhes: {task.getTitle()}")
        modal.geometry("400x550")
        modal.configure(bg="white")
        modal.grab_set()

        pos = task.getPosition()
        tk.Label(modal, text=f"{pos}. {task.getTitle()}", font=(
            "Helvetica", 16, "bold"), bg="white", fg="#2196F3", wraplength=380).pack(pady=20)

        info = tk.Frame(modal, bg="white", padx=20)
        info.pack(fill="x")

        details = [
            ("ID Coluna:", task.getColumnId()),
            ("Prazo:", task.getDeadline().strftime("%d/%m/%Y")),
            ("Posição:", str(task.getPosition()))
        ]

        for k, v in details:
            row = tk.Frame(info, bg="white")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=k, font=("bold", 10), bg="white",
                     width=12, anchor="w").pack(side="left")
            tk.Label(row, text=v, bg="white", anchor="w").pack(side="left")

        tk.Label(modal, text="Descrição:", font=("bold", 10),
                 bg="white", anchor="w").pack(fill="x", padx=20, pady=(15, 0))
        desc = tk.Label(modal, text=task.getDescription(),
                        bg="#f9f9f9", wraplength=360, justify="left", relief="solid", bd=1)
        desc.pack(fill="both", expand=True, padx=20, pady=5)

        if self.controller.user_type == "empresa":
            btn_frame = tk.Frame(modal, bg="white")
            btn_frame.pack(fill="x", pady=20, padx=20)

            tk.Button(btn_frame, text="EDITAR", bg="#FF9800", fg="white", font=("bold"),
                      command=lambda: [modal.destroy(), self.open_edit_form(task, False)]).pack(side="left", fill="x", expand=True, padx=5)

            tk.Button(btn_frame, text="EXCLUIR", bg="#f44336", fg="white", font=("bold"),
                      command=lambda: self.confirm_popup(modal, "delete", task)).pack(side="left", fill="x", expand=True, padx=5)

    def open_create_card_modal(self):
        self.open_edit_form(None, True)

    def open_edit_form(self, task_data: Card | None, is_new):
        modal = tk.Toplevel(self)
        title = "Novo Card" if is_new else "Editar Card"
        modal.title(title)
        modal.geometry("400x650")
        modal.configure(bg="white")
        modal.grab_set()

        tk.Label(modal, text=title, font=(
            "Helvetica", 14, "bold"), bg="white").pack(pady=15)

        entries = {}
        available_cols_objs: list[Column] = [c for c in Column.listAll()
                                             if c.getPublicWorkId() == self.current_work_id]

        available_cols_objs.sort(key=lambda x: x.getPosition())
        col_ids = [c.getId() for c in available_cols_objs]

        def add_field(label, key, val, kind="entry", opts=None):
            tk.Label(modal, text=label, bg="white", anchor="w").pack(
                fill="x", padx=30, pady=(5, 0))
            if kind == "entry":
                e = tk.Entry(modal, bg="#fafafa")
                e.insert(0, val)
                e.pack(fill="x", padx=30)
                entries[key] = e
            elif kind == "text":
                e = tk.Text(modal, height=5, bg="#fafafa")
                e.insert("1.0", val)
                e.pack(fill="x", padx=30)
                entries[key] = e
            elif kind == "combo":
                e = ttk.Combobox(modal, values=opts, state="readonly")
                e.set(val)
                e.pack(fill="x", padx=30)
                entries[key] = e

        val_t = "" if is_new else task_data.getTitle()
        val_c = str(col_ids[0]) if is_new and col_ids else str(
            task_data.getColumnId())
        val_p = "" if is_new else task_data.getDeadline()
        val_pos = "" if is_new else str(task_data.getPosition())
        val_d = "" if is_new else task_data.getDescription()

        add_field("Título", "titulo", val_t)
        add_field("Posição", "posicao", val_pos)
        add_field("Colunas", "status", val_c, "combo", col_ids)
        add_field("Prazo", "previsao", val_p)
        add_field("Descrição", "descricao", val_d, "text")

        tk.Button(modal, text="SALVAR", bg="#4CAF50", fg="white", font=("bold"), pady=10,
                  command=lambda: self.confirm_popup(modal, "save", task_data, entries, is_new)).pack(fill="x", padx=30, pady=30)

    def open_column_modal(self, col_data: Column, is_new):
        modal = tk.Toplevel(self)
        title_text = "Adicionar Coluna" if is_new else "Editar Coluna"
        modal.title(title_text)
        modal.geometry("350x350")
        modal.configure(bg="white")
        modal.grab_set()

        tk.Label(modal, text=title_text, font=("Helvetica", 14,
                 "bold"), bg="white", fg="#9C27B0").pack(pady=20)

        entries = {}

        val_title = "" if is_new else col_data.getName()
        val_pos = "" if is_new else str(col_data.getPosition())

        # Campo Título
        tk.Label(modal, text="Título da Coluna:", bg="white",
                 anchor="w").pack(fill="x", padx=30, pady=(5, 0))
        entry_title = tk.Entry(modal, bg="#fafafa")
        entry_title.insert(0, val_title)
        entry_title.pack(fill="x", padx=30)
        entries['titulo'] = entry_title

        # Campo Posição
        tk.Label(modal, text="Posição (Esq. para Dir.):", bg="white",
                 anchor="w").pack(fill="x", padx=30, pady=(15, 0))
        entry_pos = tk.Entry(modal, bg="#fafafa")
        entry_pos.insert(0, val_pos)
        entry_pos.pack(fill="x", padx=30)
        entries['posicao'] = entry_pos

        if is_new:
            # Botão Salvar (Verde) para criação
            tk.Button(modal, text="Salvar Alterações", bg="#4CAF50", fg="white", font=("bold"), pady=8, width=20,
                      command=lambda: self.check_column_errors(modal, entries, col_data, True)).pack(pady=30)
        else:
            # Botões Editar e Excluir para edição
            btn_frame = tk.Frame(modal, bg="white")
            btn_frame.pack(fill="x", pady=30, padx=30)

            # Editar (Laranja)
            tk.Button(btn_frame, text="EDITAR", bg="#FF9800", fg="white", font=("bold"),
                      command=lambda: self.check_column_errors(modal, entries, col_data, False)).pack(side="left", fill="x", expand=True, padx=5)

            # Excluir (Vermelho)
            tk.Button(btn_frame, text="EXCLUIR", bg="#f44336", fg="white", font=("bold"),
                      command=lambda: self.confirm_column_delete_popup(modal, col_data)).pack(side="left", fill="x", expand=True, padx=5)

    def check_column_errors(self, parent_modal, entries, col_data: Column, is_new):
        title = entries['titulo'].get().strip()
        pos = entries['posicao'].get().strip()

        if not title:
            messagebox.showwarning(
                "Atenção", "O título da coluna não pode ser vazio.", parent=parent_modal)
            return

        if not pos:
            messagebox.showwarning(
                "Atenção", "A posição da coluna não pode ser vazia.", parent=parent_modal)
            return

        # Validação de Número Natural (Inteiro >= 1)
        if not pos.isdigit() or int(pos) < 1:
            messagebox.showwarning(
                "Atenção", "A posição deve ser um número inteiro positivo (Ex: 1, 2, 3).", parent=parent_modal)
            return

        self.confirm_column_save_popup(
            parent_modal, title, int(pos), col_data, is_new)

    def confirm_column_save_popup(self, parent_modal, title, pos, col_data: Column, is_new):
        popup = tk.Toplevel(self)
        popup.title("Confirmação")
        popup.geometry("300x150")
        popup.configure(bg="white")
        popup.grab_set()

        tk.Label(popup, text="Deseja salvar as mudanças?",
                 font=("Helvetica", 11), bg="white").pack(pady=30)

        btns = tk.Frame(popup, bg="white")
        btns.pack()

        def save_action():
            if is_new:

                column = Column(title, pos, self.current_work_id)
                column.pushDatabase()

            else:

                col_data.setName(title)
                col_data.setPosition(pos)
                col_data.pushDatabase()

            popup.destroy()
            parent_modal.destroy()
            self.update_view(self.current_work_id, self.current_work_name)
            messagebox.showinfo("Sucesso", "Alterações salvas!")

        tk.Button(btns, text="SIM", bg="#4CAF50", fg="white",
                  width=10, command=save_action).pack(side="left", padx=10)
        tk.Button(btns, text="NÃO", bg="#f44336", fg="white", width=10,
                  command=popup.destroy).pack(side="right", padx=10)

    def confirm_column_delete_popup(self, parent_modal, col_data: Column):
        popup = tk.Toplevel(self)
        popup.title("Confirmação de Exclusão")
        popup.geometry("400x180")
        popup.configure(bg="white")
        popup.grab_set()

        lbl = tk.Label(popup, text="Deseja excluir a coluna?\nTodos os cards serão deletados juntos!",
                       font=("Helvetica", 11), bg="white", fg="#d32f2f")
        lbl.pack(pady=30)

        btns = tk.Frame(popup, bg="white")
        btns.pack()

        def delete_action():
            col_data.delete()

            popup.destroy()
            parent_modal.destroy()
            self.update_view(self.current_work_id, self.current_work_name)
            messagebox.showinfo("Sucesso", "Coluna e cards excluídos.")

        tk.Button(btns, text="SIM", bg="#4CAF50", fg="white", width=10,
                  command=delete_action).pack(side="left", padx=10)
        tk.Button(btns, text="NÃO", bg="#f44336", fg="white", width=10,
                  command=popup.destroy).pack(side="right", padx=10)

    def confirm_popup(self, parent_modal, action, task_data: Card | None = None, entries: dict | None = None, is_new=False):
        popup = tk.Toplevel(self)
        popup.title("Confirmação")
        popup.geometry("300x150")
        popup.configure(bg="white")
        popup.grab_set()

        msg = "Deseja excluir este card?" if action == "delete" else "Deseja salvar as alterações?"
        tk.Label(popup, text=msg, bg="white",
                 font=("Helvetica", 11)).pack(pady=30)

        btns = tk.Frame(popup, bg="white")
        btns.pack()

        def yes():
            if action == "delete":
                task_data.delete()
            elif action == "save" and entries:
                t = entries['titulo'].get().strip()
                s = entries['status'].get().strip()
                p: str = entries['previsao'].get().strip()
                pos_str = entries['posicao'].get().strip()
                d = entries['descricao'].get("1.0", "end-1c").strip()

                if not t or not s or not p or not d or not pos_str:
                    popup.destroy()
                    messagebox.showwarning(
                        "Erro", "Todos os campos são obrigatórios.", parent=parent_modal)
                    return

                if not re.match(r"^\d{2}/\d{2}/\d{4}$", p):
                    popup.destroy()
                    messagebox.showwarning(
                        "Erro", "O Prazo deve estar no formato NN/NN/NNNN.", parent=parent_modal)
                    return

                # Validação de Número Natural (Inteiro >= 1)
                if not pos_str.isdigit() or int(pos_str) < 1:
                    popup.destroy()
                    messagebox.showwarning(
                        "Erro", "A Posição deve ser um número inteiro positivo (1, 2, 3...).", parent=parent_modal)
                    return

                new_pos = int(pos_str)
                try:
                    new_p = datetime.strptime(p, "%d/%m/%Y")
                except:
                    popup.destroy()
                    messagebox.showwarning(
                        "Erro", "Data invalida", parent=parent_modal)
                    return

                if is_new:
                    card = Card(t, d, new_pos, new_p,
                                int(s), self.current_work_id)
                    card.pushDatabase()
                else:
                    task_data.setTitle(t)
                    task_data.setColumnId(int(s))
                    task_data.setPosition(new_pos)
                    task_data.setDeadline(new_p)
                    task_data.setDescription(d)
                    task_data.pushDatabase()

            popup.destroy()
            parent_modal.destroy()
            self.update_view(self.current_work_id, self.current_work_name)

        tk.Button(btns, text="SIM", bg="#4CAF50", fg="white",
                  width=10, command=yes).pack(side="left", padx=10)
        tk.Button(btns, text="NÃO", bg="#f44336", fg="white", width=10,
                  command=popup.destroy).pack(side="right", padx=10)

    def open_docs(self):
        self.controller.show_docs_frame(
            self.current_work_id, self.current_work_name)
