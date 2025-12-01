import tkinter as tk
from tkinter import ttk, messagebox
import mock_db

class EmpresasCivilFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")
        
        self.create_widgets()

    def create_widgets(self):
        # Cabeçalho
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill="x", pady=(20, 20), padx=20)

        # Botão Voltar
        tk.Button(header_frame, text="< Sair", 
                  command=lambda: self.controller.show_frame("LoginFrame"), 
                  bg="#ddd", bd=0).pack(side="left")
        
        tk.Label(header_frame, text="Empresas Contratadas", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333").pack(side="left", padx=20)

        # Treeview (Tabela)
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20)

        cols = ("Nome", "CNPJ", "Email")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        
        self.tree.heading("Nome", text="Empresa")
        self.tree.heading("CNPJ", text="CNPJ")
        self.tree.heading("Email", text="Email")
        
        self.tree.column("Nome", width=300)
        self.tree.column("CNPJ", width=150)
        self.tree.column("Email", width=200)

        self.tree.pack(fill="both", expand=True)
        
        # Scrollbar para a tabela (boa prática)
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)

        # Preencher dados
        for emp in mock_db.EMPRESAS_DB:
            self.tree.insert("", "end", values=(emp["nome"], emp["cnpj"], emp["email"]))

        # Botão de Ação
        tk.Button(self, text="VER OBRAS DA EMPRESA", 
                  command=self.go_to_details, 
                  bg="#2196F3", fg="white", font=("bold"), pady=10).pack(fill="x", padx=20, pady=20)

        # --- CORREÇÃO: Binding de Duplo Clique ---
        # Agora ao clicar duas vezes, ele chama a mesma função do botão
        self.tree.bind("<Double-1>", lambda e: self.go_to_details())

    def go_to_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma empresa.")
            return
            
        # Pega os dados da linha selecionada
        data = self.tree.item(selected[0])['values']
        
        # Chama o controlador para trocar de tela e PASSAR DADOS
        self.controller.show_obras_frame(data[0], data[1], data[2])