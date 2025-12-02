import tkinter as tk
from tkinter import ttk, messagebox
import mock_db
import re # Para regex

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
                obra = next((o for o in mock_db.OBRAS_DB if o['id'] == self.current_work_id), None)
                if obra:
                    emp = next((e for e in mock_db.EMPRESAS_DB if e['nome'] == obra['empresa']), None)
                    if emp:
                        self.controller.show_obras_frame(emp['nome'], emp['cnpj'], emp['email'])
                    else:
                        self.controller.show_frame("EmpresasCivilFrame")

        tk.Button(left_frame, text="< Voltar", command=back, bg="#ddd", bd=0, padx=10).pack(side="left")
        
        title_prefix = "Gerenciamento: " if self.controller.user_type == "empresa" else ""
        tk.Label(left_frame, text=f"{title_prefix}{self.current_work_name}", 
                 font=("Comic Sans MS", 18, "bold"), bg="#f0f0f0", fg="#333").pack(side="left", padx=20)

        right_frame = tk.Frame(header_frame, bg="#f0f0f0")
        right_frame.pack(side="right")

        if self.controller.user_type == "empresa":
            tk.Button(right_frame, text="Acessar Documentos da Obra", 
                      command=self.open_docs, bg="#607D8B", fg="white", font=("bold"), width=25, pady=5).pack(side="top", pady=(0, 5))
            # ATUALIZADO: Texto do botão alterado conforme solicitação
            tk.Button(right_frame, text="Adicionar Card", 
                      command=self.open_create_card_modal, bg="#2196F3", fg="white", font=("bold"), width=25, pady=5).pack(side="bottom")
        else:
            tk.Button(right_frame, text="Documentos da Obra", 
                      command=self.open_docs, bg="#607D8B", fg="white", padx=10).pack()

    def setUpKanbanBoard(self):
        container = tk.Frame(self.main_content, bg="#f0f0f0")
        container.pack(fill="both", expand=True)
        
        # DEFINIÇÃO DAS COLUNAS COM POSIÇÃO VISUAL FIXA
        columns_def = [
            {"titulo": "Em Planejamento", "posicao_visual": 1},
            {"titulo": "Em Andamento", "posicao_visual": 2},
            {"titulo": "Em Verificação", "posicao_visual": 3},
            {"titulo": "Concluído", "posicao_visual": 4}
        ]
        
        # Filtra tarefas e ORDENA POR POSIÇÃO
        tasks = [t for t in mock_db.KANBAN_TASKS_DB if t['obra_id'] == self.current_work_id]
        # Ordenação crescente pela posição
        tasks.sort(key=lambda x: int(x.get('posicao', 999)))

        for idx, col_data in enumerate(columns_def):
            col_name = col_data['titulo']
            col_pos_visual = col_data['posicao_visual']

            col_frame = tk.Frame(container, bg="#e0e0e0", bd=2, relief="groove")
            container.grid_columnconfigure(idx, weight=1)
            col_frame.grid(row=0, column=idx, sticky="nsew", padx=5, pady=5)

            # ATUALIZADO: Exibição da posição no título da coluna: "1. Em Planejamento"
            header_text = f"{col_pos_visual}. {col_name}"
            tk.Label(col_frame, text=header_text, font=("Helvetica", 11, "bold"), bg="#e0e0e0", fg="#555", pady=10).pack(fill="x")
            
            col_tasks = [t for t in tasks if t['status'] == col_name]
            for task in col_tasks:
                self.createCard(col_frame, task)

    def createCard(self, parent, task):
        card = tk.Frame(parent, bg="white", bd=1, relief="raised", padx=10, pady=10)
        card.pack(fill="x", padx=10, pady=5)
        
        # ATUALIZADO: Exibição da posição no título do card: "1. Projeto Elétrico"
        pos = task.get('posicao', '?')
        display_text = f"{pos}. {task['titulo']}"
        
        lbl = tk.Label(card, text=display_text, font=("Helvetica", 10, "bold"), bg="white", wraplength=150, justify="left")
        lbl.pack(anchor="w")
        
        cmd = lambda e: self.showCardModal(task)
        card.bind("<Button-1>", cmd)
        lbl.bind("<Button-1>", cmd)
        card.configure(cursor="hand2")

    def showCardModal(self, task):
        modal = tk.Toplevel(self)
        modal.title(f"Detalhes: {task['titulo']}")
        modal.geometry("400x550")
        modal.configure(bg="white")
        modal.grab_set()

        # ATUALIZADO: Exibição da posição também no título do modal
        pos = task.get('posicao', '?')
        tk.Label(modal, text=f"{pos}. {task['titulo']}", font=("Helvetica", 16, "bold"), bg="white", fg="#2196F3", wraplength=380).pack(pady=20)
        
        info = tk.Frame(modal, bg="white", padx=20)
        info.pack(fill="x")
        
        # ATUALIZADO: Incluindo 'Posição' na lista de detalhes
        details = [
            ("Colunas:", task['status']),
            ("Prazo:", task.get('previsao', '-')),
            ("Posição:", str(task.get('posicao', '-')))
        ]

        for k, v in details:
            row = tk.Frame(info, bg="white")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=k, font=("bold", 10), bg="white", width=12, anchor="w").pack(side="left")
            tk.Label(row, text=v, bg="white", anchor="w").pack(side="left")

        tk.Label(modal, text="Descrição:", font=("bold", 10), bg="white", anchor="w").pack(fill="x", padx=20, pady=(15, 0))
        desc = tk.Label(modal, text=task.get('descricao_completa', ''), bg="#f9f9f9", wraplength=360, justify="left", relief="solid", bd=1)
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

    def open_edit_form(self, task_data, is_new):
        modal = tk.Toplevel(self)
        title = "Novo Card" if is_new else "Editar Card"
        modal.title(title)
        modal.geometry("400x650") # Aumentado para caber o campo posição
        modal.configure(bg="white")
        modal.grab_set()

        tk.Label(modal, text=title, font=("Helvetica", 14, "bold"), bg="white").pack(pady=15)
        
        entries = {}
        def add_field(label, key, val, kind="entry", opts=None):
            tk.Label(modal, text=label, bg="white", anchor="w").pack(fill="x", padx=30, pady=(5,0))
            if kind=="entry":
                e = tk.Entry(modal, bg="#fafafa"); e.insert(0, val); e.pack(fill="x", padx=30)
                entries[key] = e
            elif kind=="text":
                e = tk.Text(modal, height=5, bg="#fafafa"); e.insert("1.0", val); e.pack(fill="x", padx=30)
                entries[key] = e
            elif kind=="combo":
                e = ttk.Combobox(modal, values=opts, state="readonly"); e.set(val); e.pack(fill="x", padx=30)
                entries[key] = e

        val_t = "" if is_new else task_data['titulo']
        val_s = "Em Planejamento" if is_new else task_data['status']
        val_p = "" if is_new else task_data.get('previsao', '')
        # ATUALIZADO: Recupera valor de posição para edição
        val_pos = "" if is_new else str(task_data.get('posicao', ''))
        val_d = "" if is_new else task_data.get('descricao_completa', '')

        add_field("Título", "titulo", val_t)
        # ATUALIZADO: Campo Posição adicionado
        add_field("Posição", "posicao", val_pos)
        add_field("Colunas", "status", val_s, "combo", ["Em Planejamento", "Em Andamento", "Em Verificação", "Concluído"])
        add_field("Prazo", "previsao", val_p) 
        add_field("Descrição", "descricao", val_d, "text")

        tk.Button(modal, text="SALVAR", bg="#4CAF50", fg="white", font=("bold"), pady=10,
                  command=lambda: self.confirm_popup(modal, "save", task_data, entries, is_new)).pack(fill="x", padx=30, pady=30)

    def confirm_popup(self, parent_modal, action, task_data=None, entries=None, is_new=False):
        popup = tk.Toplevel(self)
        popup.title("Confirmação")
        popup.geometry("300x150")
        popup.configure(bg="white")
        popup.grab_set()
        
        msg = "Deseja excluir este card?" if action == "delete" else "Deseja salvar as alterações?"
        tk.Label(popup, text=msg, bg="white", font=("Helvetica", 11)).pack(pady=30)
        
        btns = tk.Frame(popup, bg="white")
        btns.pack()
        
        def yes():
            if action == "delete":
                mock_db.KANBAN_TASKS_DB.remove(task_data)
            elif action == "save":
                # --- VALIDAÇÃO DE CAMPOS ---
                t = entries['titulo'].get().strip()
                s = entries['status'].get().strip()
                p = entries['previsao'].get().strip()
                # ATUALIZADO: Pegando valor da posição
                pos_str = entries['posicao'].get().strip()
                d = entries['descricao'].get("1.0", "end-1c").strip()

                if not t or not s or not p or not d or not pos_str:
                    popup.destroy()
                    messagebox.showwarning("Erro", "Todos os campos (Título, Posição, Coluna, Prazo, Descrição) são obrigatórios.", parent=parent_modal)
                    return
                
                # --- VALIDAÇÃO DE DATA (REGEX) ---
                if not re.match(r"^\d{2}/\d{2}/\d{4}$", p):
                    popup.destroy()
                    messagebox.showwarning("Erro", "O Prazo deve estar no formato NN/NN/NNNN (Ex: 01/12/2023).", parent=parent_modal)
                    return

                # ATUALIZADO: Validação de Posição (Número natural)
                if not pos_str.isdigit() or int(pos_str) <= 0:
                    popup.destroy()
                    messagebox.showwarning("Erro", "A Posição deve ser um número inteiro positivo (1, 2, 3...).", parent=parent_modal)
                    return
                
                new_pos = int(pos_str)

                new_data = {
                    "titulo": t,
                    "status": s,
                    "posicao": new_pos,
                    "previsao": p,
                    "descricao_completa": d
                }
                if is_new:
                    new_id = 999 
                    if mock_db.KANBAN_TASKS_DB:
                         new_id = max(t['id'] for t in mock_db.KANBAN_TASKS_DB) + 1
                    
                    new_card = {"id": new_id, "obra_id": self.current_work_id, **new_data}
                    mock_db.KANBAN_TASKS_DB.append(new_card)
                else:
                    task_data.update(new_data)
            
            popup.destroy()
            parent_modal.destroy()
            self.update_view(self.current_work_id, self.current_work_name)

        tk.Button(btns, text="SIM", bg="#4CAF50", fg="white", width=10, command=yes).pack(side="left", padx=10)
        tk.Button(btns, text="NÃO", bg="#f44336", fg="white", width=10, command=popup.destroy).pack(side="right", padx=10)

    def open_docs(self):
        self.controller.show_docs_frame(self.current_work_id, self.current_work_name)
