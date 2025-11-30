import tkinter as tk
from tkinter import messagebox

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # Referência ao app principal para trocar de tela
        self.configure(bg="#f0f0f0")
        
        self.create_widgets()

    def create_widgets(self):
        # Cabeçalho
        tk.Label(self, text="Kanban de Transparência", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#333").pack(pady=(50, 10))
        tk.Label(self, text="Selecione o seu perfil de acesso", font=("Helvetica", 12), bg="#f0f0f0", fg="#666").pack(pady=5)

        # Botões de Seleção
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        # Configurações visuais dos botões
        btn_config = {'width': 15, 'font': ("Helvetica", 10, "bold"), 'pady': 5}

        tk.Button(btn_frame, text="CIVIL", command=lambda: self.setup_dynamic_area("civil"), bg="#4CAF50", fg="white", **btn_config).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="EMPRESARIAL", command=lambda: self.setup_dynamic_area("empresa"), bg="#2196F3", fg="white", **btn_config).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="GOVERNAMENTAL", command=lambda: self.setup_dynamic_area("governo"), bg="#FF9800", fg="white", **btn_config).grid(row=0, column=2, padx=10)

        # Área Dinâmica (Box Branco)
        self.dynamic_frame = tk.Frame(self, bg="white", bd=1, relief="solid", padx=20, pady=20)
        self.dynamic_frame.pack(pady=20, fill="x", padx=150)
        
        # Conteúdo inicial
        tk.Label(self.dynamic_frame, text="Selecione uma opção acima.", bg="white", fg="#888").pack()

    def setup_dynamic_area(self, user_type):
        """Limpa e redesenha a área branca"""
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        if user_type == "civil":
            tk.Label(self.dynamic_frame, text="Acesso Cidadão", font=("Helvetica", 14, "bold"), bg="white", fg="#333").pack(pady=(0, 10))
            tk.Label(self.dynamic_frame, text="Visualize empresas e obras sem senha.", bg="white").pack(pady=5)
            
            # Botão que chama a função de troca de tela no Main
            tk.Button(self.dynamic_frame, text="ENTRAR NO SISTEMA", 
                      command=lambda: self.controller.show_frame("EmpresasCivilFrame"), 
                      bg="#4CAF50", fg="white", font=("bold"), width=20).pack(pady=10)
        
        else:
            # Login simples para Empresa/Governo
            tk.Label(self.dynamic_frame, text=f"Login {user_type.capitalize()}", font=("Helvetica", 14, "bold"), bg="white").pack()
            tk.Label(self.dynamic_frame, text="E-mail:", bg="white", anchor="w").pack(fill="x")
            tk.Entry(self.dynamic_frame).pack(fill="x")
            tk.Label(self.dynamic_frame, text="Senha:", bg="white", anchor="w").pack(fill="x")
            tk.Entry(self.dynamic_frame, show="*").pack(fill="x", pady=(0, 10))
            tk.Button(self.dynamic_frame, text="ENTRAR", bg="#999", fg="white", width=20).pack()