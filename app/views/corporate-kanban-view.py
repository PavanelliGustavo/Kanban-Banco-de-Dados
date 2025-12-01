import tkinter as tk
from tkinter import ttk, messagebox
import mock_db

class CorporateKanbanViewFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")
        
        self.main_content = tk.Frame(self, bg="#f0f0f0")
        self.main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.current_work_id = None
        self.current_work_name = None

    def update_view(self, work_id, work_name):
        self.current_work_id = int(work_id)
        self.current_work_name = work_name
        
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # --- 1. CABEÇALHO ---
        self.create_header()

        # --- 2. ÁREA DO KANBAN ---
        self.create_kanban_board()

    def create_header(self):
        header_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        header_frame.pack(fill="x", pady=(0, 20))

        # Botão Voltar (Volta para CorporateViewFrame)
        tk.Button(header_frame, text="< Voltar para Obras", 
                  command=lambda: self.controller.show_corporate_dashboard(), 
                  bg="#ddd", bd=0, padx=10, pady=5).pack(side="left")

        tk.Label(header_frame, text=f"Gerenciamento: {self.current_work_name}", 
                 font=("Comic Sans MS", 18, "bold"), bg="#f0f0f0", fg="#333").pack(side="left", padx=20)

        # BOTÃO: ADICIONAR NOVO CARD
        tk.Button(header_frame, text="+ ADICIONAR CARD", 
                  command=self.open_create_card_modal, 
                  bg="#2196F3", fg="white", font=("bold"), padx=15, pady=5).pack(side="right")

    def create_kanban_board(self):
        kanban_container = tk.Frame(self.main_content, bg="#f0f0f0")
        kanban_container.pack(fill="both", expand=True)
        
        self.columns = ["Em Planejamento", "Em Andamento", "Em Verificação", "Concluído"]
        
        # Filtra tarefas da obra atual
        tasks = [t for t in mock_db.KANBAN_TASKS_DB if t['obra_id'] == self.current_work_id]

        for idx, col_name in enumerate(self.columns):
            col_frame = tk.Frame(kanban_container, bg="#e0e0e0", bd=2, relief="groove")
            kanban_container.grid_columnconfigure(idx, weight=1) 
            col_frame.grid(row=0, column=idx, sticky="nsew", padx=5, pady=5)

            tk.Label(col_frame, text=col_name, font=("Helvetica", 11, "bold"), bg="#e0e0e0", fg="#555", pady=10).pack(fill="x")

            col_tasks = [t for t in tasks if t['status'] == col_name]
            for task in col_tasks:
                self.create_card_widget(col_frame, task)

    def create_card_widget(self, parent, task_data):
        """ Cria o card visual clicável """
        card = tk.Frame(parent, bg="white", bd=1, relief="raised", padx=10, pady=10)
        card.pack(fill="x", padx=10, pady=5)
        
        lbl = tk.Label(card, text=task_data['titulo'], font=("Helvetica", 10, "bold"), bg="white", wraplength=150, justify="left")
        lbl.pack(anchor="w")
        
        # Clicar no card abre o modo de VISUALIZAÇÃO primeiro
        cmd = lambda e: self.open_view_card_modal(task_data)
        
        card.bind("<Button-1>", cmd)
        lbl.bind("<Button-1>", cmd)
        
        card.configure(cursor="hand2")
        lbl.configure(cursor="hand2")

    # -------------------------------------------------------------------------
    # FLUXO DE MODAIS: VISUALIZAR -> EDITAR -> SALVAR/EXCLUIR
    # -------------------------------------------------------------------------

    def open_view_card_modal(self, task_data):
        """ Passo 1: Abre modal de visualização (Leitura) """
        modal = tk.Toplevel(self)
        modal.title(f"Visualizar: {task_data['titulo']}")
        modal.geometry("450x500")
        modal.configure(bg="white")
        modal.grab_set()

        # Conteúdo de Leitura
        tk.Label(modal, text=task_data['titulo'], font=("Helvetica", 16, "bold"), 
                 bg="white", fg="#2196F3", wraplength=400).pack(pady=20)

        info_frame = tk.Frame(modal, bg="white", padx=20)
        info_frame.pack(fill="x")

        def add_info(label, val):
            row = tk.Frame(info_frame, bg="white")
            row.pack(fill="x", pady=5)
            tk.Label(row, text=label, font=("bold", 10), bg="white", width=15, anchor="w").pack(side="left")
            tk.Label(row, text=val, bg="white", anchor="w", wraplength=280, justify="left").pack(side="left", fill="x")

        add_info("Status:", task_data['status'])
        add_info("Responsável:", task_data.get('responsavel', '-'))
        add_info("Previsão:", task_data.get('previsao', '-'))
        
        tk.Label(modal, text="Descrição:", font=("bold", 10), bg="white", anchor="w").pack(fill="x", padx=20, pady=(15, 5))
        desc_box = tk.Frame(modal, bg="#f9f9f9", bd=1, relief="solid")
        desc_box.pack(fill="both", expand=True, padx=20, pady=5)
        tk.Label(desc_box, text=task_data.get('descricao_completa', ''), bg="#f9f9f9", wraplength=380, justify="left").pack(anchor="nw", padx=5, pady=5)

        # Botões de Ação
        btn_frame = tk.Frame(modal, bg="white")
        btn_frame.pack(fill="x", pady=20, padx=20)

        # Botão Editar
        tk.Button(btn_frame, text="EDITAR CARD", bg="#FF9800", fg="white", font=("bold"),
                  command=lambda: [modal.destroy(), self.open_edit_card_modal(task_data)]).pack(side="left", fill="x", expand=True, padx=5)

        # Botão Excluir
        tk.Button(btn_frame, text="EXCLUIR CARD", bg="#f44336", fg="white", font=("bold"),
                  command=lambda: self.confirm_action_popup(modal, "delete", False, task_data, None)).pack(side="left", fill="x", expand=True, padx=5)

    def open_create_card_modal(self):
        """ Abre modal vazio para criar """
        self.show_edit_form(is_new=True)

    def open_edit_card_modal(self, task_data):
        """ Passo 2: Abre modal com campos para edição """
        self.show_edit_form(is_new=False, task_data=task_data)

    def show_edit_form(self, is_new, task_data=None):
        modal = tk.Toplevel(self)
        title = "Novo Card" if is_new else f"Editando: {task_data['titulo']}"
        modal.title(title)
        modal.geometry("450x600")
        modal.configure(bg="white")
        modal.grab_set()

        tk.Label(modal, text=title, font=("Helvetica", 14, "bold"), bg="white", fg="#2196F3").pack(pady=15)

        entries = {}
        
        def add_field(label, key, default_val="", widget_type="entry", options=None):
            tk.Label(modal, text=label, font=("bold", 10), bg="white", anchor="w").pack(fill="x", padx=30, pady=(10, 0))
            if widget_type == "entry":
                comp = tk.Entry(modal, bg="#fafafa")
                comp.insert(0, default_val)
                comp.pack(fill="x", padx=30)
                entries[key] = comp
            elif widget_type == "text":
                comp = tk.Text(modal, height=5, bg="#fafafa")
                comp.insert("1.0", default_val)
                comp.pack(fill="x", padx=30)
                entries[key] = comp
            elif widget_type == "combo":
                comp = ttk.Combobox(modal, values=options, state="readonly")
                current = default_val if default_val in options else options[0]
                comp.set(current)
                comp.pack(fill="x", padx=30)
                entries[key] = comp

        val_titulo = "" if is_new else task_data['titulo']
        val_status = "Em Planejamento" if is_new else task_data['status']
        val_resp = "" if is_new else task_data.get('responsavel', '')
        val_prev = "" if is_new else task_data.get('previsao', '')
        val_desc = "" if is_new else task_data.get('descricao_completa', '')

        add_field("Título:", "titulo", val_titulo)
        add_field("Status:", "status", val_status, "combo", self.columns)
        add_field("Responsável:", "responsavel", val_resp)
        add_field("Previsão:", "previsao", val_prev)
        add_field("Descrição:", "descricao", val_desc, "text")

        # Botão Salvar (Verde) centralizado abaixo da edição
        tk.Button(modal, text="SALVAR EDIÇÕES" if not is_new else "CRIAR CARD", 
                  bg="#4CAF50", fg="white", font=("bold"), pady=10, width=20,
                  command=lambda: self.confirm_action_popup(modal, "save", is_new, task_data, entries)).pack(pady=30)

    # -------------------------------------------------------------------------
    # POP-UP CUSTOMIZADO DE CONFIRMAÇÃO
    # -------------------------------------------------------------------------
    def confirm_action_popup(self, parent_modal, action_type, is_new, task_data, entries):
        """ Cria o Pop-up customizado com botões Sim (Verde) e Não (Vermelho) """
        
        popup = tk.Toplevel(self)
        popup.title("Confirmação")
        popup.geometry("350x180")
        popup.configure(bg="white")
        popup.grab_set() 
        
        # Centralizar popup em relação ao modal
        try:
            x = parent_modal.winfo_rootx() + 50
            y = parent_modal.winfo_rooty() + 100
            popup.geometry(f"+{x}+{y}")
        except:
            pass

        # Texto da Pergunta
        if action_type == "save":
            msg = "Deseja criar este novo card?" if is_new else "Deseja salvar as edições feitas?"
        else:
            msg = "Deseja excluir esse card?"

        tk.Label(popup, text=msg, font=("Helvetica", 12), bg="white", wraplength=300).pack(pady=30)

        btn_area = tk.Frame(popup, bg="white")
        btn_area.pack()

        # Botão SIM (Verde e à Esquerda)
        tk.Button(btn_area, text="SIM", bg="#4CAF50", fg="white", font=("bold"), width=10,
                  command=lambda: self.execute_db_operation(action_type, is_new, task_data, entries, popup, parent_modal)
                 ).pack(side="left", padx=20)

        # Botão NÃO (Vermelho e à Direita)
        tk.Button(btn_area, text="NÃO", bg="#f44336", fg="white", font=("bold"), width=10,
                  command=popup.destroy
                 ).pack(side="right", padx=20)

    def execute_db_operation(self, action_type, is_new, task_data, entries, popup, parent_modal):
        """ Executa a alteração no mock_db e fecha as janelas """
        
        if action_type == "save":
            new_data = {
                "titulo": entries['titulo'].get(),
                "status": entries['status'].get(),
                "responsavel": entries['responsavel'].get(),
                "previsao": entries['previsao'].get(),
                "descricao_completa": entries['descricao'].get("1.0", "end-1c").strip()
            }

            if is_new:
                new_id = max([t['id'] for t in mock_db.KANBAN_TASKS_DB] or [0]) + 1
                new_card = {
                    "id": new_id,
                    "obra_id": self.current_work_id,
                    **new_data
                }
                mock_db.KANBAN_TASKS_DB.append(new_card)
            else:
                task_data.update(new_data)

        elif action_type == "delete":
            mock_db.KANBAN_TASKS_DB.remove(task_data)

        # Fecha popup e modal
        popup.destroy()
        parent_modal.destroy()
        
        # Atualiza a tela principal do Kanban
        self.update_view(self.current_work_id, self.current_work_name)
