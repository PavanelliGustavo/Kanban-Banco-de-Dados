import tkinter as tk
from tkinter import ttk, messagebox
import mock_db

class ObrasEmpresaFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")
        
        self.content_frame = tk.Frame(self, bg="#f0f0f0")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def update_view(self, company_name, company_cnpj, company_email):
        # Limpar tela anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # --- CABEÇALHO ---
        header_frame = tk.Frame(self.content_frame, bg="white", bd=1, relief="solid", padx=15, pady=15)
        header_frame.pack(fill="x", pady=(0, 20)) 

        top_bar = tk.Frame(header_frame, bg="white")
        top_bar.pack(fill="x", pady=(0, 10)) 
        
        tk.Button(top_bar, text="< Voltar", 
                  command=lambda: self.controller.show_frame("EmpresasCivilFrame"), 
                  bg="#eee", bd=0, cursor="hand2").pack(side="left")
        
        tk.Label(top_bar, text=company_name, font=("Helvetica", 16, "bold"), bg="white", fg="#2196F3").pack(side="left", padx=15)

        info_grid = tk.Frame(header_frame, bg="white")
        info_grid.pack(fill="x")
        tk.Label(info_grid, text=f"CNPJ: {company_cnpj}   |   Contato: {company_email}", bg="white", fg="#555").pack(anchor="w")

        # --- FILTROS ---
        filter_frame = tk.Frame(self.content_frame, bg="#e0e0e0", padx=10, pady=10)
        filter_frame.pack(fill="x", pady=(0, 10))

        tk.Label(filter_frame, text="Ordenar:", bg="#e0e0e0").pack(side="left")
        
        self.combo_sort = ttk.Combobox(
            filter_frame, 
            values=["A-Z", "Z-A", "Recentes", "Antigas"], 
            width=15, 
            state="readonly"
        )
        self.combo_sort.current(0)
        self.combo_sort.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Aplicar", command=self.apply_filter, bg="#FF9800", fg="white").pack(side="left", padx=10)
        
        # Botão de Ação explícito (além do duplo clique)
        tk.Button(filter_frame, text="ABRIR KANBAN DA OBRA", command=self.open_kanban, bg="#4CAF50", fg="white", font=("bold", 9)).pack(side="right")

        # --- LISTA DE OBRAS ---
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill="both", expand=True)

        cols = ("Nome", "Local", "Status", "Data")
        self.works_tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        self.works_tree.heading("Nome", text="Obra")
        self.works_tree.heading("Local", text="Local")
        self.works_tree.heading("Status", text="Status")
        self.works_tree.heading("Data", text="Início")
        
        self.works_tree.pack(fill="both", expand=True)

        # Binding de Duplo Clique
        self.works_tree.bind("<Double-1>", lambda e: self.open_kanban())

        # Carregar dados iniciais
        self.current_company = company_name
        self.load_data()

    def load_data(self):
        self.works_data = [obra for obra in mock_db.OBRAS_DB if obra['empresa'] == self.current_company]
        self.populate_tree(self.works_data)

    def populate_tree(self, data):
        for item in self.works_tree.get_children():
            self.works_tree.delete(item)
        for obra in data:
            # IMPORTANTE: Usamos o iid=obra['id'] para guardar o ID real do banco na linha da tabela
            self.works_tree.insert("", "end", iid=obra['id'], values=(obra['nome'], obra['local'], obra['status'], obra['data_inicio']))

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
        """Captura a obra selecionada e abre o Kanban"""
        selected = self.works_tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma obra para visualizar o Kanban.")
            return

        # O 'selected[0]' agora retorna o ID que definimos no iid (ex: 101, 102)
        work_id = selected[0]
        
        # Pegar o nome da obra também (está na coluna 0 da tabela)
        work_name = self.works_tree.item(work_id)['values'][0]

        # Navegar
        self.controller.show_kanban_frame(work_id, work_name)