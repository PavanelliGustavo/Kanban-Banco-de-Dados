import tkinter as tk

class GovUsersSelectionView(tk.Frame):

    # region ---------------- WINDOW VARIABLES ----------------
    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"
    
    CONTENT_PARAMS = {"bg": WINDOW_BACKGROUND_COLOR}
    CONTENT_PACK = {"fill": "both", "expand": True, "padx": 40, "pady": 40}
    # endregion

    # region ---------------- HEADER VARIABLES ----------------
    HEADER_BG = "#f0f0f0"
    
    BACK_BTN_TEXT = "< Voltar"
    BACK_BTN_BG = "#ddd"
    BACK_BTN_PARAMS = {"bg": BACK_BTN_BG, "bd": 0, "padx": 10, "pady": 5}
    
    TITLE_TEXT = "Gerenciar Usuários"
    TITLE_SIZE = 24
    TITLE_STYLE = "bold"
    TITLE_FG = "#333"
    TITLE_PARAMS = {"font": (TEXT_FONT, TITLE_SIZE, TITLE_STYLE), "bg": HEADER_BG, "fg": TITLE_FG}
    
    SUBTITLE_TEXT = "Selecione o tipo de conta para administrar"
    SUBTITLE_PARAMS = {"font": (TEXT_FONT, 12), "bg": HEADER_BG, "fg": "#666"}
    # endregion

    # region ---------------- BUTTONS VARIABLES ----------------
    # Botões maiores (padrão igualamos ao CRUD Menu aumentado)
    BTN_WIDTH = 32
    BTN_HEIGHT = 6
    BTN_FONT = (TEXT_FONT, 14, "bold")
    BTN_CURSOR = "hand2"
    BTN_BORDER = {"bd": 0} 
    
    # Cores padronizadas com a Central Governamental
    
    # Botão Governamental (Esquerda - Cor do 'Gerenciar Usuários')
    BTN_GOV_TEXT = "Governamental"
    BTN_GOV_BG = "#673AB7" # Roxo / Azul Escuro
    BTN_GOV_FG = "white"
    
    # Botão Empresarial (Direita - Cor do 'Empresas')
    BTN_EMP_TEXT = "Empresarial"
    BTN_EMP_BG = "#009688" # Verde Mar / Teal
    BTN_EMP_FG = "white"
    
    # Espaçamento entre os botões (para afastar do centro)
    BTN_PADX_CONTAINER = 40
    # endregion

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)
        
        self.content = tk.Frame(self, **self.CONTENT_PARAMS)
        self.content.pack(**self.CONTENT_PACK)
        
        self.createWidgets()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpButtons()

    def setUpHeader(self):
        header = tk.Frame(self.content, bg=self.HEADER_BG)
        header.pack(fill="x", pady=(0, 40))
        
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        # Voltar
        tk.Button(header, text=self.BACK_BTN_TEXT, 
                  command=lambda: self.controller.show_frame("GovCentralViewFrame"),
                  **self.BACK_BTN_PARAMS).grid(row=0, column=0, sticky="w")
        
        # Títulos
        title_frame = tk.Frame(header, bg=self.HEADER_BG)
        title_frame.grid(row=0, column=1)
        tk.Label(title_frame, text=self.TITLE_TEXT, **self.TITLE_PARAMS).pack()
        tk.Label(title_frame, text=self.SUBTITLE_TEXT, **self.SUBTITLE_PARAMS).pack(pady=(5,0))
        
        # Espaçador
        tk.Label(header, text=self.BACK_BTN_TEXT, bg=self.HEADER_BG, fg=self.HEADER_BG, padx=10).grid(row=0, column=2)

    def setUpButtons(self):
        container = tk.Frame(self.content, bg=self.WINDOW_BACKGROUND_COLOR)
        container.pack(expand=True)

        # Botão Governamental (Esquerda)
        tk.Button(container, text=self.BTN_GOV_TEXT, bg=self.BTN_GOV_BG, fg=self.BTN_GOV_FG,
                  font=self.BTN_FONT, width=self.BTN_WIDTH, height=self.BTN_HEIGHT,
                  cursor=self.BTN_CURSOR, **self.BTN_BORDER,
                  command=lambda: self.goToCRUD("Governamental")).pack(side="left", padx=self.BTN_PADX_CONTAINER)

        # Botão Empresarial (Direita)
        tk.Button(container, text=self.BTN_EMP_TEXT, bg=self.BTN_EMP_BG, fg=self.BTN_EMP_FG,
                  font=self.BTN_FONT, width=self.BTN_WIDTH, height=self.BTN_HEIGHT,
                  cursor=self.BTN_CURSOR, **self.BTN_BORDER,
                  command=lambda: self.goToCRUD("Empresarial")).pack(side="left", padx=self.BTN_PADX_CONTAINER)

    def goToCRUD(self, user_type):
        self.controller.show_gov_crud_frame(user_type)
