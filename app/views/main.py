import tkinter as tk
from login import LoginFrame
from empresas_civil import EmpresasCivilFrame
from obras_empresa import ObrasEmpresaFrame
from kanban_view import KanbanViewFrame
from docs_view import DocsViewFrame # Importando nova view

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kanban de Transparência")
        self.geometry("1000x700")
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Registrando as classes de Frames
        for F in (LoginFrame, EmpresasCivilFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Inicializa frames dinâmicos
        self.frames["ObrasEmpresaFrame"] = ObrasEmpresaFrame(parent=self.container, controller=self)
        self.frames["ObrasEmpresaFrame"].grid(row=0, column=0, sticky="nsew")

        self.frames["KanbanViewFrame"] = KanbanViewFrame(parent=self.container, controller=self)
        self.frames["KanbanViewFrame"].grid(row=0, column=0, sticky="nsew")

        self.frames["DocsViewFrame"] = DocsViewFrame(parent=self.container, controller=self)
        self.frames["DocsViewFrame"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

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
        """Exibe a página de documentos"""
        frame = self.frames["DocsViewFrame"]
        frame.update_view(work_id, work_name)
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()