import tkinter as tk
from login import LoginFrame
from empresas_civil import EmpresasCivilFrame
from obras_empresa import ObrasEmpresaFrame
from kanban_view import KanbanViewFrame
from docs_view import DocsViewFrame 

class App(tk.Tk):

    # region ---------------- WINDOW VARIABLES ----------------

    WINDOW_TITLE = "Kanban de Transparência"
    WINDOW_GEOMETRY = "1000x700"
    
    CONTAINER_PACK_PARAMS = {"side": "top", "fill": "both", "expand": True}

    # endregion --------------------------------------------------

    def __init__(self):
        super().__init__()
        
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

        # 1. Registrando frames estáticos (sem construtor customizado além de parent/controller)
        for F in (LoginFrame, EmpresasCivilFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # 2. Registrando frames que carregam dados dinâmicos
        # Nota: Instanciamos normalmente, os dados são carregados via update_view depois
        
        self.frames["ObrasEmpresaFrame"] = ObrasEmpresaFrame(parent=self.container, controller=self)
        self.frames["ObrasEmpresaFrame"].grid(row=0, column=0, sticky="nsew")

        self.frames["KanbanViewFrame"] = KanbanViewFrame(parent=self.container, controller=self)
        self.frames["KanbanViewFrame"].grid(row=0, column=0, sticky="nsew")

        self.frames["DocsViewFrame"] = DocsViewFrame(parent=self.container, controller=self)
        self.frames["DocsViewFrame"].grid(row=0, column=0, sticky="nsew")

    # region ---------------- NAVIGATION METHODS ----------------

    def show_frame(self, page_name):
        """Traz a tela solicitada para o topo da pilha"""
        frame = self.frames[page_name]
        frame.tkraise()

    def show_obras_frame(self, nome, cnpj, email):
        """Navega para a lista de obras de uma empresa específica"""
        frame = self.frames["ObrasEmpresaFrame"]
        frame.update_view(nome, cnpj, email)
        frame.tkraise()

    def show_kanban_frame(self, work_id, work_name):
        """Navega para o Kanban de uma obra específica"""
        frame = self.frames["KanbanViewFrame"]
        frame.update_view(work_id, work_name)
        frame.tkraise()
        
    def show_docs_frame(self, work_id, work_name):
        """Navega para a página de documentos de uma obra específica"""
        frame = self.frames["DocsViewFrame"]
        frame.update_view(work_id, work_name)
        frame.tkraise()

    # endregion ---------------------------------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()
