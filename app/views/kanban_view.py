import tkinter as tk
from tkinter import messagebox
import mock_db

class KanbanViewFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")
        
        # Frame Principal de Conteúdo
        self.main_content = tk.Frame(self, bg="#f0f0f0")
        self.main_content.pack(fill="both", expand=True, padx=20, pady=20)

    def update_view(self, work_id, work_name):
        """Reconstrói o Kanban para a obra selecionada"""
        
        # Limpar tela
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # --- 1. CABEÇALHO ---
        header_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        header_frame.pack(fill="x", pady=(0, 20))

        # Botão Voltar (precisamos saber para qual empresa voltar, 
        # mas por simplificação, voltaremos para o login ou podemos passar a empresa depois)
        # Ajuste: O botão volta para a lista de empresas por segurança neste fluxo
        tk.Button(header_frame, text="< Voltar", 
                  command=lambda: self.controller.show_frame("EmpresasCivilFrame"), # Simplificação de fluxo
                  bg="#ddd", bd=0).pack(side="left")

        # Título da Obra (Centralizado conforme desenho)
        tk.Label(header_frame, text=work_name, font=("Comic Sans MS", 20, "bold"), bg="#f0f0f0", fg="#333").pack(side="top")

        # --- 2. ÁREA DO KANBAN (COLUNAS) ---
        kanban_container = tk.Frame(self.main_content, bg="#f0f0f0")
        kanban_container.pack(fill="both", expand=True)
        
        # Definição das Colunas
        columns = ["Em Planejamento", "Em Andamento", "Em Verificação", "Concluído"]
        
        # Filtrar tarefas desta obra
        tasks = [t for t in mock_db.KANBAN_TASKS_DB if t['obra_id'] == int(work_id)]

        for idx, col_name in enumerate(columns):
            # Frame da Coluna
            col_frame = tk.Frame(kanban_container, bg="#e0e0e0", bd=2, relief="groove")
            # Grid layout: 1 linha, 4 colunas. Weight 1 faz elas dividirem o espaço igualmente
            kanban_container.grid_columnconfigure(idx, weight=1) 
            col_frame.grid(row=0, column=idx, sticky="nsew", padx=5, pady=5)

            # Título da Coluna
            tk.Label(col_frame, text=col_name, font=("Helvetica", 11, "bold"), bg="#e0e0e0", fg="#555", pady=10).pack(fill="x")

            # Buscar tarefas desta coluna
            col_tasks = [t for t in tasks if t['status'] == col_name]

            # Criar os Cards
            for task in col_tasks:
                self.create_card(col_frame, task)

    def create_card(self, parent_col, task_data):
        """Desenha um card individual"""
        # Card Frame (simulando borda arredondada com relief raised)
        card = tk.Frame(parent_col, bg="white", bd=1, relief="raised", padx=10, pady=10)
        card.pack(fill="x", padx=10, pady=5)
        
        # Título da Tarefa
        lbl_title = tk.Label(card, text=task_data['titulo'], font=("Helvetica", 10, "bold"), bg="white", wraplength=150)
        lbl_title.pack(anchor="w")

        # Previsão (Info extra)
        if task_data.get('previsao'):
            tk.Label(card, text=f"Prev: {task_data['previsao']}", font=("Helvetica", 8), fg="#777", bg="white").pack(anchor="w", pady=(5,0))

        # --- INTERATIVIDADE ---
        # Ao clicar no Card ou no Label, abre detalhes (futuro)
        card.bind("<Button-1>", lambda e: self.open_card_details(task_data))
        lbl_title.bind("<Button-1>", lambda e: self.open_card_details(task_data))

        # Cursor de mãozinha
        card.configure(cursor="hand2")
        lbl_title.configure(cursor="hand2")

    def open_card_details(self, task_data):
        messagebox.showinfo("Detalhes do Card", f"Aqui abrirá a página detalhada para:\n\nTarefa: {task_data['titulo']}\nID: {task_data['id']}")