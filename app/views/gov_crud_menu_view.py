import tkinter as tk
from tkinter import messagebox
import random # Apenas para simular dados aleatórios na visualização

class GovCRUDMenuView(tk.Frame):

    # region ---------------- WINDOW VARIABLES ----------------
    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"
    # endregion

    # region ---------------- HEADER VARIABLES ----------------
    HEADER_BG = "#f0f0f0"
    TITLE_FONT = (TEXT_FONT, 20, "bold")
    TITLE_FG = "#333"
    # endregion

    # region ---------------- BUTTONS VARIABLES ----------------
    BTN_WIDTH = 32
    BTN_HEIGHT = 6
    BTN_FONT = (TEXT_FONT, 14, "bold")
    BTN_FG = "white"
    
    BTN_COLOR_1 = "#673AB7" # Roxo
    BTN_COLOR_2 = "#009688" # Verde Mar
    
    BTN_BORDER_PARAMS = {"bd": 0}
    BTN_CURSOR = "hand2"
    # endregion

    # region ---------------- MODAL STYLE ----------------
    MODAL_BG = "white"
    MODAL_FONT_LABEL = (TEXT_FONT, 10, "bold")
    MODAL_FONT_ENTRY = (TEXT_FONT, 10)
    MODAL_BTN_BG = "#4CAF50" # Verde para ações positivas
    MODAL_BTN_FG = "white"
    # endregion

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)
        
        self.content = tk.Frame(self, bg=self.WINDOW_BACKGROUND_COLOR)
        self.content.pack(fill="both", expand=True, padx=40, pady=40)
        
        self.current_user_type = ""
        self.createWidgets()

    def update_view(self, user_type):
        self.current_user_type = user_type
        self.title_label.config(text=f"Gerenciar {user_type}")

    def createWidgets(self):
        self.setUpHeader()
        self.setUpCRUDButtons()

    def setUpHeader(self):
        header = tk.Frame(self.content, bg=self.HEADER_BG)
        header.pack(fill="x", pady=(0, 40))
        
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        tk.Button(header, text="< Voltar", bg="#ddd", bd=0, padx=10, pady=5,
                  command=lambda: self.controller.show_frame("GovUsersSelectionView")).grid(row=0, column=0, sticky="w")
        
        self.title_label = tk.Label(header, text="Gerenciar ...", font=self.TITLE_FONT, bg=self.HEADER_BG, fg=self.TITLE_FG)
        self.title_label.grid(row=0, column=1)

        tk.Label(header, text="< Voltar", bg=self.HEADER_BG, fg=self.HEADER_BG, padx=10).grid(row=0, column=2)

    def setUpCRUDButtons(self):
        grid_container = tk.Frame(self.content, bg=self.WINDOW_BACKGROUND_COLOR)
        grid_container.pack(expand=True)

        buttons = [
            ("Criar", lambda: self.openFormModal("create"), self.BTN_COLOR_1),
            ("Atualizar", lambda: self.openFormModal("update"), self.BTN_COLOR_2),
            ("Visualizar", lambda: self.openFormModal("read"), self.BTN_COLOR_2),
            ("Deletar", self.actionDelete, self.BTN_COLOR_1)
        ]

        for i, (text, cmd, bg_color) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = tk.Button(grid_container, text=text, command=cmd,
                            bg=bg_color, fg=self.BTN_FG, font=self.BTN_FONT,
                            width=self.BTN_WIDTH, height=self.BTN_HEIGHT,
                            cursor=self.BTN_CURSOR, **self.BTN_BORDER_PARAMS)
            btn.grid(row=row, column=col, padx=40, pady=30)

    # region ---------------- FORM MODAL LOGIC ----------------

    def openFormModal(self, action_type):
        """
        Abre o formulário modal configurado para Criar, Ler ou Atualizar.
        action_type: 'create', 'read', 'update'
        """
        
        # Configuração da Janela
        modal = tk.Toplevel(self)
        title_map = {"create": "Criar Novo Usuário", "read": "Visualizar Usuário", "update": "Atualizar Usuário"}
        modal.title(f"{title_map[action_type]} - {self.current_user_type}")
        modal.geometry("450x500")
        modal.configure(bg=self.MODAL_BG)
        
        modal.wait_visibility()
        modal.grab_set()

        # Título do Modal
        tk.Label(modal, text=title_map[action_type], font=("Helvetica", 16, "bold"), 
                 bg=self.MODAL_BG, fg="#333").pack(pady=20)

        # Campos do Formulário
        form_frame = tk.Frame(modal, bg=self.MODAL_BG)
        form_frame.pack(fill="both", expand=True, padx=40)

        # Definição dos campos baseados no tipo de usuário
        fields_config = []
        
        # ID é comum a todos (Sempre readonly)
        # Em um caso real, buscaríamos o próximo ID do banco
        fake_next_id = str(random.randint(1000, 9999)) 
        fields_config.append({"label": "ID:", "key": "id", "value": fake_next_id, "state": "readonly"})

        if self.current_user_type == "Governamental":
            fields_config.append({"label": "Nome do Departamento:", "key": "dept_name", "value": ""})
            fields_config.append({"label": "E-mail:", "key": "email", "value": ""})
            fields_config.append({"label": "Senha:", "key": "password", "value": "", "show": "*"})
        
        elif self.current_user_type == "Empresarial":
            fields_config.append({"label": "CNPJ:", "key": "cnpj", "value": ""})
            fields_config.append({"label": "Nome Fantasia:", "key": "name", "value": ""})
            fields_config.append({"label": "E-mail:", "key": "email", "value": ""})
            fields_config.append({"label": "Senha:", "key": "password", "value": "", "show": "*"})

        # Renderização dos Campos
        self.entries = {}
        
        for field in fields_config:
            # Container do campo
            row = tk.Frame(form_frame, bg=self.MODAL_BG)
            row.pack(fill="x", pady=5)
            
            tk.Label(row, text=field["label"], font=self.MODAL_FONT_LABEL, 
                     bg=self.MODAL_BG, anchor="w").pack(fill="x")
            
            # Valor Inicial (Para Read/Update simulamos dados)
            initial_value = field["value"]
            if action_type in ["read", "update"] and field["key"] != "id":
                initial_value = f"Valor Simulado {field['key']}" # Mock de dados existentes
            
            # Estado do campo
            state = "normal"
            if action_type == "read" or field.get("state") == "readonly":
                state = "readonly"
            
            entry = tk.Entry(row, font=self.MODAL_FONT_ENTRY, bg="#f9f9f9", 
                             state="normal") # Criamos como normal para inserir texto
            
            entry.insert(0, initial_value)
            
            if field.get("show"): # Máscara de senha
                # Se for visualização, talvez não devêssemos mostrar a senha, mas seguindo o pedido:
                if action_type != "read": 
                    entry.config(show="*")
            
            # Aplica o estado final (travado se for readonly)
            entry.config(state=state)
            
            entry.pack(fill="x", pady=(2, 0), ipady=3)
            self.entries[field["key"]] = entry

        # Botão de Ação
        btn_text = ""
        btn_cmd = None
        
        if action_type == "create":
            btn_text = "CRIAR USUÁRIO"
            btn_cmd = lambda: self.submitForm(modal, "criado")
        elif action_type == "update":
            btn_text = "SALVAR ALTERAÇÕES"
            btn_cmd = lambda: self.submitForm(modal, "atualizado")
        elif action_type == "read":
            btn_text = "FECHAR"
            btn_bg = "#757575" # Cinza para fechar
            btn_cmd = modal.destroy

        # Renderiza botão se houver texto
        if btn_text:
            bg_color = self.MODAL_BTN_BG if action_type != "read" else "#757575"
            tk.Button(modal, text=btn_text, bg=bg_color, fg=self.MODAL_BTN_FG, 
                      font=("Helvetica", 11, "bold"), pady=10, bd=0,
                      command=btn_cmd).pack(fill="x", padx=40, pady=30)

    def submitForm(self, modal, action_verb):
        # Aqui capturaríamos self.entries['key'].get() para salvar no banco
        messagebox.showinfo("Sucesso", f"Usuário {self.current_user_type} foi {action_verb} com sucesso!")
        modal.destroy()

    def actionDelete(self):
        # Para deletar, geralmente não precisamos de form complexo, apenas ID ou seleção
        # Simulando um popup de ID
        id_popup = tk.Toplevel(self)
        id_popup.title("Deletar")
        id_popup.geometry("300x150")
        id_popup.configure(bg="white")
        
        tk.Label(id_popup, text="Informe o ID para deletar:", bg="white", font=("bold", 10)).pack(pady=10)
        entry_id = tk.Entry(id_popup)
        entry_id.pack(pady=5)
        
        def confirm():
            if entry_id.get():
                if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o usuário ID {entry_id.get()}?"):
                    messagebox.showinfo("Deletado", "Usuário removido do banco de dados.")
                    id_popup.destroy()
        
        tk.Button(id_popup, text="DELETAR", bg="#f44336", fg="white", font=("bold"), command=confirm).pack(pady=10)

    # endregion
