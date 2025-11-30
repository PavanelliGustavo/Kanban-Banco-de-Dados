import tkinter as tk
from app.views.login import LoginScreen
from app.views.search_companies import CompaniesSearchScreen


class App(tk.Tk):

    # region ---------------- WINDOW VARIABLES ----------------

    WINDOW_TITLE_TEXT = "Kanban de Transparência - Obras Públicas"
    WINDOW_BACKGROUND_COLOR: str = "#f0f0f0"
    WINDOW_DIMENSIONS = "600x500"
    WINDOW_START_AT_FULL_SCREEN = True

    # endregion -----------------------------------------------

    def __init__(self):
        super().__init__()

        self.title(self.WINDOW_TITLE_TEXT)
        self.geometry(self.WINDOW_DIMENSIONS)
        self.attributes("-zoomed", self.WINDOW_START_AT_FULL_SCREEN)
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)

        self.frames: dict[str, tk.Frame] = {}
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        for screen in (CompaniesSearchScreen, LoginScreen):
            frame = screen(container, controller=self)
            self.frames[screen.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, tela: str):
        self.frames[tela].tkraise()
