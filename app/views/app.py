import tkinter as tk
from app.views.login import LoginFrame
from app.views.corporate_view import ObrasEmpresaFrame
from app.views.kanban_view import KanbanViewFrame
from app.views.docs_view import DocsViewFrame
from app.views.empresas_civil import EmpresasCivilFrame


class App(tk.Tk):

    # region ---------------- WINDOW VARIABLES ----------------

    WINDOW_TITLE = "Kanban de Transparência"
    WINDOW_GEOMETRY = "1000x700"

    CONTAINER_PACK_PARAMS = {"side": "top", "fill": "both", "expand": True}

    # endregion --------------------------------------------------

    def __init__(self):
        super().__init__()

        # --- ESTADO DO USUÁRIO ---
        # "civil" = Apenas Leitura
        # "empresa" = Leitura e Escrita
        self.user_type = None
        self.user_id = None   # ID da empresa logada (se for empresa)

        self.setUpWindow()
        self.setUpContainer()
        self.registerFrames()

        # Tela Inicial
        self.show_frame("LoginFrame")

    def setUpWindow(self):
        self.title(self.WINDOW_TITLE)
        self.geometry(self.WINDOW_GEOMETRY)

    def setUpContainer(self):
        self.container = tk.Frame(self)
        self.container.pack(**self.CONTAINER_PACK_PARAMS)

        # Configuração de Grid para empilhamento (Stack)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def registerFrames(self):
        self.frames = {}

        # Registramos apenas as views originais. A lógica interna delas mudará conforme o user_type.
        for F in (LoginFrame, EmpresasCivilFrame, ObrasEmpresaFrame, KanbanViewFrame, DocsViewFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    # region ---------------- NAVIGATION METHODS ----------------

    def show_frame(self, page_name):
        """Traz a tela solicitada para o topo da pilha"""
        frame = self.frames[page_name]

        # Se for logout (voltando para login), limpa sessão
        if page_name == "LoginFrame":
            self.user_type = None
            self.user_id = None

        frame.tkraise()

    def show_obras_frame(self, nome=None, cnpj=None, email=None):
        """
        Navega para a lista de obras.
        - Se Civil: Recebe 'nome', 'cnpj', 'email' da seleção anterior.
        - Se Empresa: O frame ObrasEmpresaFrame vai usar self.user_id para se auto-preencher.
        """
        frame = self.frames["ObrasEmpresaFrame"]
        frame.update_view(nome, cnpj, email)
        frame.tkraise()

    def show_kanban_frame(self, work_id, work_name):
        """Navega para o Kanban de uma obra específica"""
        frame = self.frames["KanbanViewFrame"]
        frame.update_view(work_id, work_name)
        frame.tkraise()

    def show_docs_frame(self, work_id, work_name):
        """Navega para a página de documentos"""
        frame = self.frames["DocsViewFrame"]
        frame.update_view(work_id, work_name)
        frame.tkraise()
