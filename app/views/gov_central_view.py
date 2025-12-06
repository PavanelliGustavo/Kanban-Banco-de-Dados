import tkinter as tk
from tkinter import messagebox

class GovCentralViewFrame(tk.Frame):

    # region ---------------- WINDOW VARIABLES ----------------

    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"
    
    CONTENT_FRAME_BG = "#f0f0f0"
    CONTENT_FRAME_PARAMS = {"fill": "both", 
                            "expand": True, 
                            "padx": 40, 
                            "pady": 40}

    # endregion --------------------------------------------------

    # region ---------------- HEADER VARIABLES ----------------

    HEADER_BG = "#f0f0f0"
    HEADER_PACK_PADY = (0, 40)

    # Botão Sair
    LOGOUT_BTN_TEXT = "Sair"
    LOGOUT_BTN_BG = "#ddd"
    LOGOUT_BTN_BD = 0
    LOGOUT_BTN_PARAMS = {"bg": LOGOUT_BTN_BG, "bd": LOGOUT_BTN_BD, "padx": 15, "pady": 5}
    
    # Título
    TITLE_TEXT = "Central Governamental"
    TITLE_SIZE = 24
    TITLE_STYLE = "bold"
    TITLE_FG = "#333"

    # Subtítulo
    SUBTITLE_TEXT = "Selecione o módulo de gestão desejado"
    SUBTITLE_SIZE = 12
    SUBTITLE_FG = "#666"

    # endregion ---------------------------------------------------

    # region ---------------- BUTTONS AREA VARIABLES ----------------

    BUTTONS_FRAME_BG = "#f0f0f0"
    
    BIG_BTN_WIDTH = 30
    BIG_BTN_HEIGHT = 5
    BIG_BTN_FONT_SIZE = 12
    BIG_BTN_FONT_STYLE = "bold"
    BIG_BTN_FG = "white"
    BIG_BTN_CURSOR = "hand2"
    
    BIG_BTN_PADX = 20

    # Botão Gerenciar Usuários
    BTN_USERS_TEXT = "Gerenciar Usuários"
    BTN_USERS_BG = "#673AB7" # Roxo
    
    # Botão Empresas/Obras
    BTN_COMPANIES_TEXT = "Gestão de Obras & Empresas"
    BTN_COMPANIES_BG = "#009688" # Teal/Verde Água

    # endregion ---------------------------------------------------

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)
        
        self.main_content = tk.Frame(self, bg=self.CONTENT_FRAME_BG)
        self.main_content.pack(**self.CONTENT_FRAME_PARAMS)

        self.createWidgets()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpButtonsArea()

    def setUpHeader(self):
        header_frame = tk.Frame(self.main_content, bg=self.HEADER_BG)
        header_frame.pack(fill="x", pady=self.HEADER_PACK_PADY)

        header_frame.grid_columnconfigure(0, weight=0) 
        header_frame.grid_columnconfigure(1, weight=1) 
        header_frame.grid_columnconfigure(2, weight=0) 

        tk.Button(header_frame, text=self.LOGOUT_BTN_TEXT, 
                  command=lambda: self.controller.show_frame("LoginFrame"),
                  **self.LOGOUT_BTN_PARAMS).grid(row=0, column=0, sticky="w")

        title_container = tk.Frame(header_frame, bg=self.HEADER_BG)
        title_container.grid(row=0, column=1)

        tk.Label(title_container, text=self.TITLE_TEXT, 
                 font=(self.TEXT_FONT, self.TITLE_SIZE, self.TITLE_STYLE), 
                 bg=self.HEADER_BG, fg=self.TITLE_FG).pack()
        
        tk.Label(title_container, text=self.SUBTITLE_TEXT, 
                 font=(self.TEXT_FONT, self.SUBTITLE_SIZE), 
                 bg=self.HEADER_BG, fg=self.SUBTITLE_FG).pack(pady=(5,0))
        
        tk.Label(header_frame, text=self.LOGOUT_BTN_TEXT, 
                 bg=self.HEADER_BG, fg=self.HEADER_BG, 
                 padx=15, pady=5).grid(row=0, column=2, sticky="e")

    def setUpButtonsArea(self):
        buttons_container = tk.Frame(self.main_content, bg=self.BUTTONS_FRAME_BG)
        buttons_container.pack(expand=True)

        btn_users = tk.Button(buttons_container, text=self.BTN_USERS_TEXT,
                              bg=self.BTN_USERS_BG, fg=self.BIG_BTN_FG,
                              font=(self.TEXT_FONT, self.BIG_BTN_FONT_SIZE, self.BIG_BTN_FONT_STYLE),
                              width=self.BIG_BTN_WIDTH, height=self.BIG_BTN_HEIGHT,
                              cursor=self.BIG_BTN_CURSOR, bd=0,
                              command=self.openUsersManager)
        btn_users.pack(side="left", padx=self.BIG_BTN_PADX)

        btn_companies = tk.Button(buttons_container, text=self.BTN_COMPANIES_TEXT,
                                  bg=self.BTN_COMPANIES_BG, fg=self.BIG_BTN_FG,
                                  font=(self.TEXT_FONT, self.BIG_BTN_FONT_SIZE, self.BIG_BTN_FONT_STYLE),
                                  width=self.BIG_BTN_WIDTH, height=self.BIG_BTN_HEIGHT,
                                  cursor=self.BIG_BTN_CURSOR, bd=0,
                                  command=self.openCompaniesFlow)
        btn_companies.pack(side="left", padx=self.BIG_BTN_PADX)

    # region ---------------- NAVIGATION ACTIONS ----------------

    def openUsersManager(self):
        # AQUI ESTÁ A LIGAÇÃO: Vai para a tela de Seleção
        self.controller.show_frame("GovUsersSelectionView")

    def openCompaniesFlow(self):
        self.controller.show_frame("EmpresasCivilFrame")

    # endregion ---------------------------------------------------