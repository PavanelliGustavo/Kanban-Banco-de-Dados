import tkinter as tk
from tkinter import ttk, messagebox
import mock_db

class EmpresasCivilFrame(tk.Frame):

    # region ---------------- WINDOW VARIABLES ----------------

    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"

    # endregion --------------------------------------------------

    # region ---------------- HEADER VARIABLES ----------------

    HEADER_BG = "#f0f0f0"
    HEADER_PACK_PADY = (20, 20)
    HEADER_PACK_PADX = 20

    # Botão Sair
    EXIT_BUTTON_TEXT = "< Sair"
    EXIT_BUTTON_BG = "#ddd"
    EXIT_BUTTON_BD = 0
    
    # Título Principal
    TITLE_TEXT = "Empresas Contratadas"
    TITLE_FONT_SIZE = 18
    TITLE_FONT_STYLE = "bold"
    TITLE_FG = "#333"

    # endregion ---------------------------------------------------

    # region ---------------- LIST VARIABLES ----------------

    LIST_FRAME_PACK_PADX = 20
    
    TREE_COLUMNS = ("Nome", "CNPJ", "Email")
    
    COL_NOME_WIDTH = 300
    COL_CNPJ_WIDTH = 150
    COL_EMAIL_WIDTH = 200

    # endregion ---------------------------------------------------

    # region ---------------- ACTION BUTTON VARIABLES ----------------

    ACTION_BTN_TEXT = "VER OBRAS DA EMPRESA"
    ACTION_BTN_BG = "#2196F3"
    ACTION_BTN_FG = "white"
    ACTION_BTN_FONT_STYLE = "bold"
    ACTION_BTN_PADY = 10
    
    ACTION_BTN_PACK_PADX = 20
    ACTION_BTN_PACK_PADY = 20

    # endregion ---------------------------------------------------

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)
        
        self.createWidgets()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpCompanyList()
        self.setUpActionButton()

    def setUpHeader(self):
        header_frame = tk.Frame(self, bg=self.HEADER_BG)
        header_frame.pack(fill="x", pady=self.HEADER_PACK_PADY, padx=self.HEADER_PACK_PADX)

        # Botão Voltar
        def exit_command(): return self.controller.show_frame("LoginFrame")
        
        tk.Button(header_frame, text=self.EXIT_BUTTON_TEXT, command=exit_command, 
                  bg=self.EXIT_BUTTON_BG, bd=self.EXIT_BUTTON_BD).pack(side="left")
        
        # Título
        tk.Label(header_frame, text=self.TITLE_TEXT, 
                 font=(self.TEXT_FONT, self.TITLE_FONT_SIZE, self.TITLE_FONT_STYLE), 
                 bg=self.HEADER_BG, fg=self.TITLE_FG).pack(side="left", padx=20)

    def setUpCompanyList(self):
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=self.LIST_FRAME_PACK_PADX)

        self.tree = ttk.Treeview(tree_frame, columns=self.TREE_COLUMNS, show="headings")
        
        # Configuração das Colunas
        self.tree.heading("Nome", text="Empresa")
        self.tree.heading("CNPJ", text="CNPJ")
        self.tree.heading("Email", text="Email")
        
        self.tree.column("Nome", width=self.COL_NOME_WIDTH)
        self.tree.column("CNPJ", width=self.COL_CNPJ_WIDTH)
        self.tree.column("Email", width=self.COL_EMAIL_WIDTH)

        self.tree.pack(fill="both", expand=True)
        
        # Scrollbar
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)

        # Preencher dados
        self.populateTree()

        # Binding de Duplo Clique
        self.tree.bind("<Double-1>", lambda e: self.go_to_details())

    def setUpActionButton(self):
        tk.Button(self, text=self.ACTION_BTN_TEXT, command=self.go_to_details, 
                  bg=self.ACTION_BTN_BG, fg=self.ACTION_BTN_FG, 
                  font=(self.TEXT_FONT, 10, self.ACTION_BTN_FONT_STYLE), 
                  pady=self.ACTION_BTN_PADY).pack(fill="x", 
                                                  padx=self.ACTION_BTN_PACK_PADX, 
                                                  pady=self.ACTION_BTN_PACK_PADY)

    def populateTree(self):
        # Limpa dados existentes (caso a tela seja recarregada)
        for item in self.tree.get_children():
            self.tree.delete(item)

        for emp in mock_db.EMPRESAS_DB:
            self.tree.insert("", "end", values=(emp["nome"], emp["cnpj"], emp["email"]))

    def go_to_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma empresa.")
            return
            
        # Pega os dados da linha selecionada
        data = self.tree.item(selected[0])['values']
        
        # Chama o controlador para trocar de tela e PASSAR DADOS
        self.controller.show_obras_frame(data[0], data[1], data[2])import tkinter as tk



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
