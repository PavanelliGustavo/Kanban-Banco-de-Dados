import tkinter as tk
from tkinter import ttk, messagebox
from app.models.model_corporate_user import Corporate


class CompaniesSearchScreen(tk.Frame):

    # region ---------------- WINDOW STYLE ----------------

    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"

    # endregion -------------------------------------------

    # region ---------------- HEADER STYLE ----------------

    HEADER_FRAME_PADDING = (20, 20)
    HEADER_LEFT_BUTTON_BG = "#ddd"
    HEADER_LEFT_BUTTON_TEXT = "< Sair"
    HEADER_LEFT_BUTTON_PARAMS = {
        "text": HEADER_LEFT_BUTTON_TEXT,
        "bg": HEADER_LEFT_BUTTON_BG,
        "bd": 0
    }

    HEADER_TITLE_TEXT = "Empresas Contratadas"
    HEADER_TITLE_COLOR = "#333"
    HEADER_TITLE_SIZE = 18
    HEADER_TITLE_STYLE = "bold"
    HEADER_TITLE_PARAMS = {
        "text": HEADER_TITLE_TEXT,
        "font": (TEXT_FONT, HEADER_TITLE_SIZE, HEADER_TITLE_STYLE),
        "bg": WINDOW_BACKGROUND_COLOR,
        "fg": HEADER_TITLE_COLOR
    }

    # endregion -------------------------------------------

    # region ---------------- TABLE STYLE -----------------

    TABLE_COLUMNS = ("Nome", "CNPJ", "Email")

    TABLE_COLUMN_WIDTHS = {
        "Nome": 300,
        "CNPJ": 150,
        "Email": 200
    }

    TABLE_EXTERNAL_PADDING = 20

    # endregion -------------------------------------------

    # region ------------ ACTION BUTTON STYLE -------------

    ACTION_BUTTON_TEXT = "VER OBRAS DA EMPRESA"
    ACTION_BUTTON_BG = "#2196F3"
    ACTION_BUTTON_FG = "white"
    ACTION_BUTTON_FONT = (TEXT_FONT, 10, "bold")
    ACTION_BUTTON_PARAMS = {
        "text": ACTION_BUTTON_TEXT,
        "bg": ACTION_BUTTON_BG,
        "fg": ACTION_BUTTON_FG,
        "font": ACTION_BUTTON_FONT,
        "pady": 10
    }
    ACTION_BUTTON_PACK_PARAMS = {
        "fill": "x",
        "padx": 20,
        "pady": 20
    }

    # endregion -------------------------------------------

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)

        self.createWidgets()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpTable()
        self.populateTable()
        self.setUpActionButton()
        self.bindTableDoubleClick()

    def setUpHeader(self):
        header_frame = tk.Frame(self, bg=self.WINDOW_BACKGROUND_COLOR)
        header_frame.pack(fill="x", pady=self.HEADER_FRAME_PADDING, padx=20)

        back_button = tk.Button(
            header_frame,
            command=self.goBack,
            **self.HEADER_LEFT_BUTTON_PARAMS
        )
        back_button.pack(side="left")

        title_label = tk.Label(header_frame, **self.HEADER_TITLE_PARAMS)
        title_label.pack(side="left", padx=20)

    def goBack(self):
        self.controller.show_frame("LoginScreen")

    def setUpTable(self):
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True,
                         padx=self.TABLE_EXTERNAL_PADDING)

        self.tree = ttk.Treeview(table_frame, show="headings",
                                 columns=self.TABLE_COLUMNS)

        for col in self.TABLE_COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=self.TABLE_COLUMN_WIDTHS[col])

        self.tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def populateTable(self):
        self.tree.delete(*self.tree.get_children())

        for corp in Corporate.listAll():
            values = corp.getData()
            self.tree.insert("", "end", values=(values["company_name"],
                                                values["cnpj"],
                                                values["email"]))

    def setUpActionButton(self):
        action_button = tk.Button(self, command=self.goToDetails,
                                  **self.ACTION_BUTTON_PARAMS)
        action_button.pack(**self.ACTION_BUTTON_PACK_PARAMS)

    def bindTableDoubleClick(self):
        self.tree.bind("<Double-1>", lambda e: self.goToDetails())

    def getSelectedCompany(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma empresa.")
            return None

        return self.tree.item(selected[0])["values"]

    def goToDetails(self):
        data = self.getSelectedCompany()
        if not data:
            return
        nome, cnpj, email = data
        self.controller.show_obras_frame(nome, cnpj, email)
