import tkinter as tk
from login import LoginFrame
from empresas_civil import EmpresasCivilFrame
from obras_empresa import ObrasEmpresaFrame
from kanban_view import KanbanViewFrame
from docs_view import DocsViewFrame 
from gov_central_view import GovCentralViewFrame
# Novas Telas
from gov_users_selection_view import GovUsersSelectionView
from gov_crud_menu_view import GovCRUDMenuView

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
        
        self.show_frame("LoginFrame")

    def setUpWindow(self):
        self.title(self.WINDOW_TITLE)
        self.geometry(self.WINDOW_GEOMETRY)

    def setUpContainer(self):
        self.container = tk.Frame(self)
        self.container.pack(**self.CONTAINER_PACK_PARAMS)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def registerFrames(self):
        self.frames = {}

        # Registrando frames estáticos
        for F in (LoginFrame, EmpresasCivilFrame, GovCentralViewFrame, GovUsersSelectionView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Registrando frames dinâmicos
        self.frames["ObrasEmpresaFrame"] = ObrasEmpresaFrame(parent=self.container, controller=self)
        self.frames["ObrasEmpresaFrame"].grid(row=0, column=0, sticky="nsew")

        self.frames["KanbanViewFrame"] = KanbanViewFrame(parent=self.container, controller=self)
        self.frames["KanbanViewFrame"].grid(row=0, column=0, sticky="nsew")

        self.frames["DocsViewFrame"] = DocsViewFrame(parent=self.container, controller=self)
        self.frames["DocsViewFrame"].grid(row=0, column=0, sticky="nsew")
        
        self.frames["GovCRUDMenuView"] = GovCRUDMenuView(parent=self.container, controller=self)
        self.frames["GovCRUDMenuView"].grid(row=0, column=0, sticky="nsew")

    # region ---------------- NAVIGATION METHODS ----------------

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def show_obras_frame(self, nome, cnpj, email):
        frame = self.frames["ObrasEmpresaFrame"]
        frame.update_view(nome, cnpj, email)
        frame.tkraise()

    def show_kanban_frame(self, work_id, work_name):
        frame = self.frames["KanbanViewFrame"]
        frame.update_view(work_id, work_name)
        frame.tkraise()
        
    def show_docs_frame(self, work_id, work_name):
        frame = self.frames["DocsViewFrame"]
        frame.update_view(work_id, work_name)
        frame.tkraise()
        
    def show_gov_crud_frame(self, user_type):
        """Navega para o menu CRUD com o tipo de usuário selecionado"""
        frame = self.frames["GovCRUDMenuView"]
        frame.update_view(user_type)
        frame.tkraise()

    # endregion ---------------------------------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()