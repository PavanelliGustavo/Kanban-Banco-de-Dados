import tkinter as tk
from tkinter import ttk, messagebox
import mock_db

class KanbanViewFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")
        
        # Frame Principal
        self.main_content = tk.Frame(self, bg="#f0f0f0")
        self.main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.current_work_id = None
        self.current_work_name = None

    def update_view(self, work_id, work_name):
        """Reconstrói o Kanban para a obra selecionada"""
        self.current_work_id = work_id
        self.current_work_name = work_name
        
        # Limpar tela
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # --- 1. CABEÇALHO ---
        header_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        header_frame.pack(fill="x", pady=(0, 20))

        # Botão Voltar
        tk.Button(header_frame, text="< Voltar", 
                  command=lambda: self.controller.show_frame("EmpresasCivilFrame"), 
                  bg="#ddd", bd=0).pack(side="left")

        # Título da Obra (Centralizado)
        title_frame = tk.Frame(header_frame, bg="#f0f0f0")
        title_frame.pack(side="left", expand=True, fill="x")
        tk.Label(title_frame, text=work_name, font=("Comic Sans MS", 20, "bold"), bg="#f0f0f0", fg="#333").pack()

        # Botão DOCUMENTOS (ATUALIZADO)
        tk.Button(header_frame, text="Acessar Documentos da Obra", 
                  command=self.open_documents_page, 
                  bg="#607D8B", fg="white", font=("Helvetica", 10, "bold"), padx=10).pack(side="right")

        # --- 2. ÁREA DO KANBAN ---
        kanban_container = tk.Frame(self.main_content, bg="#f0f0f0")
        kanban_container.pack(fill="both", expand=True)
        
        columns = ["Em Planejamento", "Em Andamento", "Em Verificação", "Concluído"]
        tasks = [t for t in mock_db.KANBAN_TASKS_DB if t['obra_id'] == int(work_id)]

        for idx, col_name in enumerate(columns):
            # Frame da Coluna
            col_frame = tk.Frame(kanban_container, bg="#e0e0e0", bd=2, relief="groove")
            kanban_container.grid_columnconfigure(idx, weight=1) 
            col_frame.grid(row=0, column=idx, sticky="nsew", padx=5, pady=5)

            # Título da Coluna
            tk.Label(col_frame, text=col_name, font=("Helvetica", 11, "bold"), bg="#e0e0e0", fg="#555", pady=10).pack(fill="x")

            # Buscar tarefas desta coluna
            col_tasks = [t for t in tasks if t['status'] == col_name]

            for task in col_tasks:
                self.create_card(col_frame, task)

    def create_card(self, parent_col, task_data):
        """Desenha um card individual"""
        card = tk.Frame(parent_col, bg="white", bd=1, relief="raised", padx=10, pady=10)
        card.pack(fill="x", padx=10, pady=5)
        
        lbl_title = tk.Label(card, text=task_data['titulo'], font=("Helvetica", 10, "bold"), bg="white", wraplength=150, justify="left")
        lbl_title.pack(anchor="w")

        if task_data.get('previsao'):
            tk.Label(card, text=f"Prev: {task_data['previsao']}", font=("Helvetica", 8), fg="#777", bg="white").pack(anchor="w", pady=(5,0))

        # Bindings para abrir o modal
        card.bind("<Button-1>", lambda e: self.show_card_modal(task_data))
        lbl_title.bind("<Button-1>", lambda e: self.show_card_modal(task_data))
        
        # Cursor
        card.configure(cursor="hand2")
        lbl_title.configure(cursor="hand2")

    def show_card_modal(self, task):
        """Cria uma janela modal (popup) customizada com os detalhes"""
        
        modal = tk.Toplevel(self)
        modal.title(f"Detalhes: {task['titulo']}")
        modal.geometry("400x500")
        modal.configure(bg="white")
        
        # Garante compatibilidade Linux
        modal.wait_visibility() 
        modal.transient(self) 
        modal.grab_set()

        # Conteúdo do Modal
        tk.Label(modal, text=task['titulo'], font=("Helvetica", 16, "bold"), bg="white", fg="#2196F3", wraplength=380).pack(pady=(20, 10))
        
        # Status Badge
        status_color = "#FFC107"
        if task['status'] == "Concluído": status_color = "#4CAF50"
        elif task['status'] == "Em Andamento": status_color = "#2196F3"
        
        lbl_status = tk.Label(modal, text=task['status'].upper(), font=("Helvetica", 9, "bold"), bg=status_color, fg="white", padx=10, pady=2)
        lbl_status.pack(pady=(0, 20))

        # Info Grid
        info_frame = tk.Frame(modal, bg="white", padx=20)
        info_frame.pack(fill="x")

        def add_detail(label, value):
            row = tk.Frame(info_frame, bg="white")
            row.pack(fill="x", pady=5)
            tk.Label(row, text=label, font=("Helvetica", 10, "bold"), bg="white", width=15, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Helvetica", 10), bg="white", anchor="w", wraplength=230, justify="left").pack(side="left", fill="x")

        add_detail("Responsável:", task.get('responsavel', 'Não informado'))
        add_detail("Previsão/Status:", task.get('previsao', '-'))
        
        # Divisor
        ttk.Separator(modal, orient='horizontal').pack(fill='x', padx=20, pady=15)

        # Descrição Completa
        tk.Label(modal, text="Descrição da Atividade:", font=("Helvetica", 11, "bold"), bg="white", anchor="w").pack(fill="x", padx=20)
        
        desc_frame = tk.Frame(modal, bg="#f9f9f9", bd=1, relief="solid")
        desc_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        tk.Label(desc_frame, text=task.get('descricao_completa', 'Sem descrição detalhada.'), 
                 bg="#f9f9f9", wraplength=340, justify="left", padx=10, pady=10).pack(fill="both", expand=True, anchor="nw")

        # Botão Fechar
        tk.Button(modal, text="Fechar", command=modal.destroy, bg="#ddd", width=10).pack(pady=15)

    def open_documents_page(self):
        # Chama a nova página via controlador
        self.controller.show_docs_frame(self.current_work_id, self.current_work_name)