import tkinter as tk
from tkinter import ttk, messagebox
import mock_db

class DocsViewFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")
        
        self.main_content = tk.Frame(self, bg="#f0f0f0")
        self.main_content.pack(fill="both", expand=True, padx=40, pady=40)
        
        self.current_work_id = None
        self.current_work_name = None
        self.current_docs = [] # Lista para armazenar documentos atuais e permitir ordenação

    def update_view(self, work_id, work_name):
        self.current_work_id = work_id
        self.current_work_name = work_name
        
        # Limpar tela
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # --- 1. CABEÇALHO ---
        header_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        header_frame.pack(fill="x", pady=(0, 20))

        # Botão Voltar
        tk.Button(header_frame, text="< Voltar para o Kanban", 
                  command=lambda: self.controller.show_kanban_frame(self.current_work_id, self.current_work_name), 
                  bg="#ddd", bd=0, padx=10, pady=5).pack(side="left")
        
        # Título
        tk.Label(header_frame, text="Documentos", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#333").pack(side="left", padx=30)
        tk.Label(header_frame, text=f"Referente a: {work_name}", font=("Helvetica", 10, "italic"), bg="#f0f0f0", fg="#666").pack(side="bottom", anchor="w")

        # --- 2. ÁREA DE FILTROS (NOVA) ---
        filter_frame = tk.Frame(self.main_content, bg="#e0e0e0", padx=10, pady=10)
        filter_frame.pack(fill="x", pady=(0, 10))

        tk.Label(filter_frame, text="Ordenar arquivos por:", bg="#e0e0e0").pack(side="left")
        
        self.combo_sort = ttk.Combobox(
            filter_frame, 
            values=["A-Z (Nome)", "Z-A (Nome)", "Mais Recentes", "Mais Antigos"], 
            width=20, 
            state="readonly"
        )
        self.combo_sort.current(2) # Padrão: Mais Recentes
        self.combo_sort.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Aplicar Ordem", command=self.apply_sort, bg="#FF9800", fg="white").pack(side="left", padx=10)

        # --- 3. LISTA DE DOCUMENTOS ---
        tree_frame = tk.Frame(self.main_content)
        tree_frame.pack(fill="both", expand=True)

        cols = ("Documento", "Tipo", "Data")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=10)
        
        self.tree.heading("Documento", text="Nome do Arquivo")
        self.tree.heading("Tipo", text="Formato")
        self.tree.heading("Data", text="Data de Publicação")
        
        self.tree.column("Documento", width=400)
        self.tree.column("Tipo", width=100, anchor="center")
        self.tree.column("Data", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, side="left")
        
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)

        # Carregar Dados Iniciais
        if hasattr(mock_db, 'DOCUMENTS_DB'):
            self.current_docs = [d for d in mock_db.DOCUMENTS_DB if d['obra_id'] == int(work_id)]
        else:
            self.current_docs = []

        # Aplica a ordenação inicial (Mais Recentes) e popula a tabela
        self.apply_sort()

        # Bind duplo clique
        self.tree.bind("<Double-1>", self.on_open_document)

        # Botão Ação
        tk.Button(self.main_content, text="ABRIR DOCUMENTO SELECIONADO", 
                  command=self.on_open_document, 
                  bg="#607D8B", fg="white", font=("bold"), pady=10).pack(fill="x", pady=20)

    def populate_tree(self, data):
        """Limpa e preenche a tabela"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not data:
            self.tree.insert("", "end", values=("Nenhum documento encontrado.", "-", "-"))
        else:
            for doc in data:
                self.tree.insert("", "end", iid=doc['id'], values=(doc['titulo'], doc['tipo'], doc['data']))

    def apply_sort(self):
        """Ordena a lista self.current_docs baseado na seleção"""
        sort_opt = self.combo_sort.get()
        
        # Trabalhamos com uma cópia para não bagunçar a referência original se necessário
        # mas aqui podemos ordenar self.current_docs direto
        
        if sort_opt == "A-Z (Nome)":
            self.current_docs.sort(key=lambda x: x['titulo'])
        elif sort_opt == "Z-A (Nome)":
            self.current_docs.sort(key=lambda x: x['titulo'], reverse=True)
        elif sort_opt == "Mais Recentes":
            # Datas YYYY-MM-DD ordenam corretamente como string
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