import tkinter as tk
from tkinter import messagebox

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
    # Botões ainda maiores conforme solicitado
    BTN_WIDTH = 32
    BTN_HEIGHT = 6
    BTN_FONT = (TEXT_FONT, 14, "bold")
    BTN_FG = "white"
    
    # Cores vindas da Central Governamental
    BTN_COLOR_1 = "#673AB7" # Roxo / Azul Escuro
    BTN_COLOR_2 = "#009688" # Verde Mar / Teal
    
    BTN_BORDER_PARAMS = {"bd": 0} # Sem borda para estilo "flat" moderno
    BTN_CURSOR = "hand2"
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
        """Atualiza a tela com o tipo de usuário selecionado"""
        self.current_user_type = user_type
        # Atualiza o título dinamicamente
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

        # Botão Voltar para a Seleção
        tk.Button(header, text="< Voltar", bg="#ddd", bd=0, padx=10, pady=5,
                  command=lambda: self.controller.show_frame("GovUsersSelectionView")).grid(row=0, column=0, sticky="w")
        
        # Título que será atualizado dinamicamente
        self.title_label = tk.Label(header, text="Gerenciar ...", font=self.TITLE_FONT, bg=self.HEADER_BG, fg=self.TITLE_FG)
        self.title_label.grid(row=0, column=1)

        # Espaçador
        tk.Label(header, text="< Voltar", bg=self.HEADER_BG, fg=self.HEADER_BG, padx=10).grid(row=0, column=2)

    def setUpCRUDButtons(self):
        # Container central (Grid 2x2)
        grid_container = tk.Frame(self.content, bg=self.WINDOW_BACKGROUND_COLOR)
        grid_container.pack(expand=True)

        # Tupla: (Texto, Comando, Cor de Fundo)
        # Intercalando as cores para visual dinâmico
        buttons = [
            ("Criar", self.actionCreate, self.BTN_COLOR_1),
            ("Atualizar", self.actionUpdate, self.BTN_COLOR_2),
            ("Visualizar", self.actionRead, self.BTN_COLOR_2),
            ("Deletar", self.actionDelete, self.BTN_COLOR_1)
        ]

        for i, (text, cmd, bg_color) in enumerate(buttons):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(grid_container, text=text, command=cmd,
                            bg=bg_color, fg=self.BTN_FG, font=self.BTN_FONT,
                            width=self.BTN_WIDTH, height=self.BTN_HEIGHT,
                            cursor=self.BTN_CURSOR, **self.BTN_BORDER_PARAMS)
            
            # Aumentei o padding do grid para afastar do centro (padx/pady maiores)
            btn.grid(row=row, column=col, padx=40, pady=30)

    # region ---------------- ACTIONS ----------------
    def actionCreate(self):
        messagebox.showinfo("Ação", f"Criar novo usuário {self.current_user_type}")

    def actionUpdate(self):
        messagebox.showinfo("Ação", f"Atualizar usuário {self.current_user_type}")

    def actionRead(self):
        messagebox.showinfo("Ação", f"Visualizar lista de {self.current_user_type}")

    def actionDelete(self):
        messagebox.showinfo("Ação", f"Deletar usuário {self.current_user_type}")
    # endregion