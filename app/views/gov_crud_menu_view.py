import tkinter as tk
from tkinter import messagebox, simpledialog
from app.db.database_connection import Database

class GovCRUDMenuView(tk.Frame):

    # region ---------------- CONFIGURAÇÕES VISUAIS ----------------
    WINDOW_BG = "#f0f0f0"
    
    # Cores
    COLOR_PRIMARY = "#2196F3"    # Azul
    COLOR_SUCCESS = "#4CAF50"    # Verde
    COLOR_WARNING = "#FF9800"    # Laranja
    COLOR_DANGER = "#F44336"     # Vermelho
    COLOR_NEUTRAL = "#9E9E9E"    # Cinza
    
    FONT_TITLE = ("Helvetica", 18, "bold")
    FONT_LABEL = ("Helvetica", 10)
    FONT_ENTRY = ("Helvetica", 10)
    # endregion

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BG)
        
        # Variáveis de Estado
        self.current_user_type = "" # "Governamental" ou "Empresarial"
        
        self.create_widgets()

    def update_view(self, user_type):
        self.current_user_type = user_type
        if hasattr(self, 'lbl_main_title'):
            self.lbl_main_title.config(text=f"Gerenciar: {user_type}")

    def create_widgets(self):
        # --- HEADER ---
        header = tk.Frame(self, bg=self.WINDOW_BG)
        header.pack(fill="x", pady=20, padx=20)
        
        btn_back = tk.Button(header, text="< Voltar", bg="#ddd", bd=0, padx=15, pady=5,
                             command=lambda: self.controller.show_frame("GovUsersSelectionView"))
        btn_back.pack(side="left")

        self.lbl_main_title = tk.Label(header, text="Gerenciar", font=("Helvetica", 20, "bold"), 
                                       bg=self.WINDOW_BG, fg="#333")
        self.lbl_main_title.pack(side="left", padx=20)

        # --- BOTÕES DO MENU ---
        container_btns = tk.Frame(self, bg=self.WINDOW_BG)
        container_btns.pack(expand=True)

        btn_opts = {
            "font": ("Helvetica", 12, "bold"), "fg": "white", "width": 25, "height": 3, "bd": 0, "cursor": "hand2"
        }

        tk.Button(container_btns, text="CRIAR NOVO", bg=self.COLOR_SUCCESS, command=lambda: self.open_modal("create"), **btn_opts)\
            .grid(row=0, column=0, padx=20, pady=20)

        tk.Button(container_btns, text="EDITAR EXISTENTE", bg=self.COLOR_WARNING, command=lambda: self.ask_id_and_open("update"), **btn_opts)\
            .grid(row=0, column=1, padx=20, pady=20)

        tk.Button(container_btns, text="VISUALIZAR DADOS", bg=self.COLOR_PRIMARY, command=lambda: self.ask_id_and_open("read"), **btn_opts)\
            .grid(row=1, column=0, padx=20, pady=20)

        tk.Button(container_btns, text="EXCLUIR REGISTRO", bg=self.COLOR_DANGER, command=self.delete_record, **btn_opts)\
            .grid(row=1, column=1, padx=20, pady=20)


    # region ---------------- LÓGICA DE BANCO DE DADOS ----------------

    def fetch_data(self, record_id):
        try:
            if self.current_user_type == "Governamental":
                query = f"SELECT id, department_name, email, password FROM tb_government WHERE id = {record_id}"
                rows = Database.select(query)
                if rows:
                    return {"id": rows[0][0], "dept_name": rows[0][1], "email": rows[0][2], "password": rows[0][3]}
            
            elif self.current_user_type == "Empresarial":
                # CORREÇÃO: Coluna 'company_name' alterada para 'name'
                query = f"SELECT id, name, cnpj, email, password FROM tb_corporate WHERE id = {record_id}"
                rows = Database.select(query)
                if rows:
                    return {"id": rows[0][0], "name": rows[0][1], "cnpj": rows[0][2], "email": rows[0][3], "password": rows[0][4]}
            
            return None
        except Exception as e:
            messagebox.showerror("Erro de DB", f"Falha na busca: {e}")
            return None

    def delete_record(self):
        record_id = simpledialog.askinteger("Excluir", "Informe o ID para excluir:")
        if not record_id: return

        if not messagebox.askyesno("Atenção", "Tem certeza? Essa ação não pode ser desfeita."):
            return

        table = "tb_government" if self.current_user_type == "Governamental" else "tb_corporate"
        try:
            Database.execute(f"DELETE FROM {table} WHERE id = {record_id}")
            messagebox.showinfo("Sucesso", "Registro removido.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # endregion


    # region ---------------- MODAL (POP-UP) ----------------

    def ask_id_and_open(self, mode):
        record_id = simpledialog.askinteger("Buscar", f"Informe o ID do usuário para {mode}:")
        if not record_id: return

        data = self.fetch_data(record_id)
        if data:
            self.open_modal(mode, data)
        else:
            messagebox.showwarning("Não encontrado", "Nenhum registro encontrado com este ID.")

    def open_modal(self, mode, data=None):
        modal = tk.Toplevel(self)
        modal.title(f"{mode.upper()} - {self.current_user_type}")
        modal.geometry("400x550")
        modal.configure(bg="white")
        modal.grab_set()

        vars_dict = {
            "dept_name": tk.StringVar(value=data['dept_name'] if data else ""),
            "cnpj": tk.StringVar(value=data['cnpj'] if data else ""),
            "name": tk.StringVar(value=data['name'] if data else ""),
            "email": tk.StringVar(value=data['email'] if data else ""),
            "password": tk.StringVar(value=data['password'] if data else "")
        }

        # --- UI DO MODAL ---
        lbl_title = "Novo Registro"
        if mode == "update": lbl_title = "Editar Registro"
        if mode == "read": lbl_title = f"Visualizar: ID {data['id']}"

        tk.Label(modal, text=lbl_title, font=("Helvetica", 16, "bold"), 
                 bg="white", fg=self.COLOR_PRIMARY).pack(pady=20)

        form_frame = tk.Frame(modal, bg="white", padx=30)
        form_frame.pack(fill="both", expand=True)

        def create_field(label_text, var_key, is_password=False):
            tk.Label(form_frame, text=label_text, font=self.FONT_LABEL, bg="white", anchor="w").pack(fill="x", pady=(10, 0))
            entry = tk.Entry(form_frame, textvariable=vars_dict[var_key], font=self.FONT_ENTRY, bg="#f9f9f9", relief="solid", bd=1)
            entry.pack(fill="x", pady=(5, 0), ipady=4)
            if is_password and mode != "read": 
                entry.config(show="*")
            if mode == "read":
                entry.config(state="readonly", fg="#666")

        if self.current_user_type == "Governamental":
            create_field("Nome do Departamento:", "dept_name")
            create_field("E-mail de Acesso:", "email")
            create_field("Senha:", "password", is_password=True)
        
        elif self.current_user_type == "Empresarial":
            create_field("CNPJ (Apenas números):", "cnpj")
            create_field("Razão Social / Nome Fantasia:", "name")
            create_field("E-mail:", "email")
            create_field("Senha:", "password", is_password=True)

        btn_text = "SALVAR"
        btn_bg = self.COLOR_SUCCESS
        cmd = None

        if mode == "create":
            btn_text = "CRIAR REGISTRO"
            cmd = lambda: self.submit_to_db(modal, "insert", vars_dict, None)
        elif mode == "update":
            btn_text = "SALVAR ALTERAÇÕES"
            btn_bg = self.COLOR_WARNING
            cmd = lambda: self.submit_to_db(modal, "update", vars_dict, data['id'])
        elif mode == "read":
            btn_text = "FECHAR"
            btn_bg = self.COLOR_NEUTRAL
            cmd = modal.destroy

        tk.Button(modal, text=btn_text, bg=btn_bg, fg="white", font=("Helvetica", 12, "bold"), 
                  bd=0, pady=10, command=cmd).pack(fill="x", padx=30, pady=30)


    def submit_to_db(self, modal, action, vars_dict, record_id):
        try:
            val_dept = vars_dict["dept_name"].get().strip()
            val_cnpj = vars_dict["cnpj"].get().strip()
            val_name = vars_dict["name"].get().strip()
            val_email = vars_dict["email"].get().strip()
            val_pass = vars_dict["password"].get().strip()

            if self.current_user_type == "Governamental":
                if not val_dept or not val_email or not val_pass:
                    messagebox.showwarning("Aviso", "Preencha todos os campos.")
                    return

                if action == "insert":
                    query = "INSERT INTO tb_government (department_name, email, password) VALUES (%s, %s, %s)"
                    Database.execute(query, (val_dept, val_email, val_pass))
                
                elif action == "update":
                    query = "UPDATE tb_government SET department_name=%s, email=%s, password=%s WHERE id=%s"
                    Database.execute(query, (val_dept, val_email, val_pass, record_id))

            elif self.current_user_type == "Empresarial":
                if not val_cnpj or not val_name:
                    messagebox.showwarning("Aviso", "CNPJ e Nome são obrigatórios.")
                    return
                
                if action == "insert":
                    # CORREÇÃO: 'company_name' alterado para 'name'
                    query = "INSERT INTO tb_corporate (cnpj, name, email, password) VALUES (%s, %s, %s, %s)"
                    Database.execute(query, (val_cnpj, val_name, val_email, val_pass))
                
                elif action == "update":
                    # CORREÇÃO: 'company_name' alterado para 'name'
                    query = "UPDATE tb_corporate SET cnpj=%s, name=%s, email=%s, password=%s WHERE id=%s"
                    Database.execute(query, (val_cnpj, val_name, val_email, val_pass, record_id))

            messagebox.showinfo("Sucesso", "Operação realizada com sucesso!")
            modal.destroy()

        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha no Banco de Dados: {e}")

    # endregion