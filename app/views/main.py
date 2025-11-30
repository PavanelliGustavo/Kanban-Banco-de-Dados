import tkinter as tk
from login import LoginFrame
from empresas_civil import EmpresasCivilFrame
from obras_empresa import ObrasEmpresaFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kanban de Transparência")
        self.geometry("900x650")
        
        # Container principal onde as telas serão empilhadas
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dicionário para guardar as telas criadas
        self.frames = {}

        # Inicializa as telas que não precisam de dados dinâmicos imediatos
        for F in (LoginFrame, EmpresasCivilFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Inicializa a tela de obras vazia (será preenchida ao ser chamada)
        frame_obras = ObrasEmpresaFrame(parent=self.container, controller=self)
        self.frames["ObrasEmpresaFrame"] = frame_obras
        frame_obras.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        """Traz a tela solicitada para o topo da pilha"""
        frame = self.frames[page_name]
        frame.tkraise()

    def show_obras_frame(self, nome, cnpj, email):
        """Função especial para carregar a tela de obras com dados"""
        frame = self.frames["ObrasEmpresaFrame"]
        # Chama o método de atualização dentro do arquivo obras_empresa.py
        frame.update_view(nome, cnpj, email)
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()