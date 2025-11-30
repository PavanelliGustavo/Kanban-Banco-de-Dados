import tkinter as tk
from tkinter import messagebox
from typing import Type
from app.models.model_corporate_user import Corporate
from app.models.model_government_user import Government
from app.models.model_user import AuthenticatedUser


class LoginScreen(tk.Frame):

    # region ---------------- WINDOW VARIABLES ----------------

    WINDOW_BACKGROUND_COLOR: str = "#f0f0f0"
    TEXT_FONT = "Helvetica"

    # endregion --------------------------------------------------

    # region ---------------- HEADER VARIABLES ----------------

    HEADER_FRAME_PADDING = 40

    HEADER_TITLE_TEXT = "Kanban de Transparência"
    HEADER_TITLE_SIZE = 24
    HEADER_TITLE_STYLE = "bold"
    HEADER_TITLE_COLOR = "#333333"
    HEADER_TITLE_PARAMS = {"text": HEADER_TITLE_TEXT,
                           "font": (TEXT_FONT, HEADER_TITLE_SIZE, HEADER_TITLE_STYLE),
                           "bg": WINDOW_BACKGROUND_COLOR,
                           "fg": HEADER_TITLE_COLOR}

    HEADER_SUBTITLE_TEXT = "Selecione o seu perfil de acesso"
    HEADER_SUBTITLE_SIZE = 12
    HEADER_SUBTITLE_COLOR = "#666666"
    HEADER_SUBTITLE_PADDING = 5
    HEADER_SUBTITLE_PARAMS = {"text": HEADER_SUBTITLE_TEXT,
                              "font": (TEXT_FONT, HEADER_SUBTITLE_SIZE),
                              "bg": WINDOW_BACKGROUND_COLOR,
                              "fg": HEADER_SUBTITLE_COLOR}

    # endregion ---------------------------------------------------

    # region ----------- USER TYPE BUTTON VARIABLES ------------

    BUTTON_FONT_COLOR = "white"
    BUTTON_COLOR_BY_USER_TYPE = {"civil": "#4CAF50",
                                 "empresarial": "#2196F3",
                                 "governamental": "#FF9800"}
    BUTTON_EXTERNAL_PADDING = 10
    BUTTON_INTERNAL_PADDING = 5
    BUTTON_WIDTH = 15
    BUTTON_FONT_SIZE = 10
    BUTTON_FONT_STYLE = "bold"
    BUTTON_CONFIG = {"width": BUTTON_WIDTH,
                     "font": (TEXT_FONT, BUTTON_FONT_SIZE, BUTTON_FONT_STYLE),
                     "pady": BUTTON_INTERNAL_PADDING}

    # endregion ---------------------------------------------------

    # region -------------- LOGIN AREA VARIABLES ---------------

    LOGIN_AREA_FRAME_COLOR = "white"
    LOGIN_AREA_BORDER_WIDTH = 1
    LOGIN_AREA_BORDER_STYLE = "solid"
    LOGIN_AREA_INTERNAL_HORIZONTAL_PADDING = 20
    LOGIN_AREA_INTERNAL_VERTICAL_PADDING = 20
    LOGIN_AREA_FRAME_PARAMS = {"bg": LOGIN_AREA_FRAME_COLOR,
                               "bd": LOGIN_AREA_BORDER_WIDTH,
                               "relief": LOGIN_AREA_BORDER_STYLE,
                               "padx": LOGIN_AREA_INTERNAL_HORIZONTAL_PADDING,
                               "pady": LOGIN_AREA_INTERNAL_VERTICAL_PADDING}

    LOGIN_AREA_EXTERNAL_HORIZONTAL_PADDING = 100
    LOGIN_AREA_EXTERNAL_VERTICAL_PADDING = 20
    LOGIN_AREA_FILL_METHOD = "x"
    LOGIN_AREA_FRAME_PACK_PARAMS = {"pady": LOGIN_AREA_EXTERNAL_VERTICAL_PADDING,
                                    "fill": LOGIN_AREA_FILL_METHOD,
                                    "padx": LOGIN_AREA_EXTERNAL_HORIZONTAL_PADDING}

    LOGIN_AREA_LABEL_TEXT = "Selecione uma opção acima para continuar."
    LOGIN_AREA_LABEL_FONT_COLOR = "#888"
    LOGIN_AREA_LABEL_PARAMS = {"text": LOGIN_AREA_LABEL_TEXT,
                               "bg": LOGIN_AREA_FRAME_COLOR,
                               "fg": LOGIN_AREA_LABEL_FONT_COLOR}

    # endregion ---------------------------------------------------

    # region ------------- LOGIN CONTENT VARIABLES --------------

    LOGIN_CONTENT_TITLE_WINDOW_BACKGROUND_COLOR = "white"
    LOGIN_CONTENT_TITLE_FONT_COLOR = "#333"

    LOGIN_CONTENT_TITLE_BY_USER_TYPE = {"civil": "Acesso Cidadão",
                                        "empresarial": "Acesso Corporativo",
                                        "governamental": "Acesso Administrativo"}
    LOGIN_CONTENT_TITLE_FONT_SIZE = 14
    LOGIN_CONTENT_TITLE_FONT_STYLE = "bold"

    LOGIN_CONTENT_TITLE_PARAMS = {"font": (TEXT_FONT,
                                           LOGIN_CONTENT_TITLE_FONT_SIZE,
                                           LOGIN_CONTENT_TITLE_FONT_STYLE),
                                  "bg": LOGIN_CONTENT_TITLE_WINDOW_BACKGROUND_COLOR,
                                  "fg": LOGIN_CONTENT_TITLE_FONT_COLOR}

    LOGIN_CONTENT_TITLE_PACK_VERTICAL_PADDING = (0, 15)

    # endregion ---------------------------------------------------

    # region -------------- CIVIL USER VARIABLES ----------------

    CIVIL_USER_LABEL_TEXT = "Visualize o andamento das obras públicas\nsem necessidade de cadastro."
    CIVIL_USER_LABEL_WINDOW_BACKGROUND_COLOR = "white",
    CIVIL_USER_LABEL_JUSTIFY = "center"
    CIVIL_USER_LABEL_PARAMS = {"text": CIVIL_USER_LABEL_TEXT,
                               "bg": CIVIL_USER_LABEL_WINDOW_BACKGROUND_COLOR,
                               "justify": CIVIL_USER_LABEL_JUSTIFY}
    CIVIL_USER_LABEL_PACK_VERTICAL_PADDING = 10

    CIVIL_USER_BUTTON_TEXT = "ENTRAR NO SISTEMA"
    CIVIL_USER_BUTTON_TEXT_SIZE = 11
    CIVIL_USER_BUTTON_TEXT_STYLE = "bold"
    CIVIL_USER_BUTTON_TEXT_COLOR = "white"
    CIVIL_USER_BUTTON_WIDTH = 20
    CIVIL_USER_BUTTON_WINDOW_BACKGROUND_COLOR = "#4CAF50"

    CIVIL_USER_BUTTON_PARAMS = {"text": CIVIL_USER_BUTTON_TEXT,
                                "bg": CIVIL_USER_BUTTON_WINDOW_BACKGROUND_COLOR,
                                "fg": CIVIL_USER_BUTTON_TEXT_COLOR,
                                "font": (TEXT_FONT, CIVIL_USER_BUTTON_TEXT_SIZE, CIVIL_USER_BUTTON_TEXT_STYLE),
                                "width": CIVIL_USER_BUTTON_WIDTH}
    CIVIL_USER_BUTTON_PACK_VERTICAL_PADDING = 10

    # endregion ---------------------------------------------------

    # region ------------- LOGIN FIELDS VARIABLES ---------------

    LOGIN_FIELD_LABEL_WINDOW_BACKGROUND_COLOR = "white"
    LOGIN_FILED_LABEL_ANCHOR = "w"
    LOGIN_FIELD_LABEL_PACK_FILL = "x"

    LOGIN_FIELD_INPUT_PACK_FILL = "x"
    LOGIN_FIELD_EMAIL_PACK_VERTICAL_PADDING = (0, 10)
    LOGIN_FIELD_PASSWORD_PACK_VERTICAL_PADDING = (0, 15)

    LOGIN_FIELD_BUTTON_WIDTH = 20
    LOGIN_FIELD_BUTTON_TEXT = "AUTENTICAR"
    LOGIN_FIELD_BUTTON_TEXT_COLOR = "white"
    LOGIN_FIELD_BUTTON_FONT_SIZE = 11
    LOGIN_FIELD_BUTTON_FONT_STYLE = "bold"
    LOGIN_FIELD_BUTTON_PARAMS = {"text": LOGIN_FIELD_BUTTON_TEXT,
                                 "fg": LOGIN_FIELD_BUTTON_TEXT_COLOR,
                                 "font": (TEXT_FONT, LOGIN_FIELD_BUTTON_FONT_SIZE, LOGIN_FIELD_BUTTON_FONT_STYLE),
                                 "width": LOGIN_FIELD_BUTTON_WIDTH}
    LOGIN_FIELD_BUTTON_PACK_VERTICAL_PADDING = 5

    # endregion ---------------------------------------------------

    def __init__(self, parent, controller):

        super().__init__(parent)
        self.controller = controller

        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)
        self.user_type = tk.StringVar(value="")
        self.createWidgets()

    def setUpHeader(self):
        header_frame = tk.Frame(self, bg=self.WINDOW_BACKGROUND_COLOR)
        header_frame.pack(pady=self.HEADER_FRAME_PADDING)

        title_label = tk.Label(header_frame, **self.HEADER_TITLE_PARAMS)
        title_label.pack()

        subtitle_label = tk.Label(header_frame, **self.HEADER_SUBTITLE_PARAMS)
        subtitle_label.pack(pady=self.HEADER_SUBTITLE_PADDING)

    def setUpAllUserTypeButtons(self):

        buttons_frame = tk.Frame(self, bg=self.WINDOW_BACKGROUND_COLOR)
        buttons_frame.pack(pady=20)

        self.setUpUserTypeButton(buttons_frame, "civil", position=0)
        self.setUpUserTypeButton(buttons_frame, "empresarial", position=1)
        self.setUpUserTypeButton(buttons_frame, "governamental", position=2)

    def setUpUserTypeButton(self, frame: tk.Frame, user_type: str, position: int):

        def command(): return self.customizeLogin(user_type)

        button_name = f"btn_{user_type}"
        button_value = tk.Button(frame, text=user_type.upper(), command=command,
                                 bg=self.BUTTON_COLOR_BY_USER_TYPE[user_type],
                                 fg=self.BUTTON_FONT_COLOR, **self.BUTTON_CONFIG)

        setattr(self, button_name, button_value)
        btn = getattr(self, button_name)
        getattr(btn, "grid")(row=0, column=position,
                             padx=self.BUTTON_EXTERNAL_PADDING)

    def setUpLoginArea(self):
        self.login_area_frame = tk.Frame(self, **self.LOGIN_AREA_FRAME_PARAMS)
        self.login_area_frame.pack(**self.LOGIN_AREA_FRAME_PACK_PARAMS)

        self.login_area_label = tk.Label(self.login_area_frame,
                                         **self.LOGIN_AREA_LABEL_PARAMS)
        self.login_area_label.pack()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpAllUserTypeButtons()
        self.setUpLoginArea()

    def clearWidgets(self):
        for widget in self.login_area_frame.winfo_children():
            widget.destroy()

    def customizeLoginContentTitle(self, user_type: str):
        title = tk.Label(self.login_area_frame,
                         text=self.LOGIN_CONTENT_TITLE_BY_USER_TYPE[user_type],
                         **self.LOGIN_CONTENT_TITLE_PARAMS)
        title.pack(pady=self.LOGIN_CONTENT_TITLE_PACK_VERTICAL_PADDING)

    def civilUserLogin(self):
        label = tk.Label(self.login_area_frame,
                         **self.CIVIL_USER_LABEL_PARAMS)

        label.pack(pady=self.CIVIL_USER_LABEL_PACK_VERTICAL_PADDING)

        button = tk.Button(self.login_area_frame, command=self.performLogin,
                           **self.CIVIL_USER_BUTTON_PARAMS)

        button.pack(pady=self.CIVIL_USER_BUTTON_PACK_VERTICAL_PADDING)

    def nonCivilUserLogin(self, user_type: str):

        self.showField("email")
        v_padding = self.LOGIN_FIELD_EMAIL_PACK_VERTICAL_PADDING
        email = self.captureFieldInput(v_padding)

        self.showField("senha")
        v_padding = self.LOGIN_FIELD_PASSWORD_PACK_VERTICAL_PADDING
        password = self.captureFieldInput(v_padding, show="*")

        def command(): return self.performLogin(email, password)

        btn_color = self.BUTTON_COLOR_BY_USER_TYPE[user_type]

        btn_login = tk.Button(self.login_area_frame, command=command,
                              bg=btn_color, **self.LOGIN_FIELD_BUTTON_PARAMS)

        btn_login.pack(pady=self.LOGIN_FIELD_BUTTON_PACK_VERTICAL_PADDING)

    def showField(self, name: str):
        field_label = tk.Label(self.login_area_frame, text=f"{name}: ",
                               bg=self.LOGIN_FIELD_LABEL_WINDOW_BACKGROUND_COLOR,
                               anchor=self.LOGIN_FILED_LABEL_ANCHOR)
        field_label.pack(fill=self.LOGIN_FIELD_LABEL_PACK_FILL)

    def captureFieldInput(self, vertical_padding: int | tuple[int], show: str = "") -> str:
        input = tk.Entry(self.login_area_frame, show=show)
        input.pack(fill=self.LOGIN_FIELD_INPUT_PACK_FILL,
                   pady=vertical_padding)
        return input

    def customizeLogin(self, user_type):

        self.user_type.set(user_type)
        self.clearWidgets()
        self.customizeLoginContentTitle(user_type)

        if user_type == "civil":
            self.civilUserLogin()
        else:
            self.nonCivilUserLogin(user_type)

    def performLogin(self, email_entry: tk.Entry | None = None, password_entry: tk.Entry | None = None):

        user_type = self.user_type.get()

        if user_type == "civil":
            self.civilValidation()
        else:
            user_type_constructor = Corporate if user_type == "corporate" else Government
            email = email_entry.get()
            password = password_entry.get()
            self.nonCivilValidation(email, password, user_type_constructor)

    def civilValidation(self):
        self.controller.show_frame("CompaniesSearchScreen")

    def nonCivilValidation(self, email: str | None, password: str | None, user_type: Type[AuthenticatedUser]):
        if not email or not password:
            warning = "Atenção", "Por favor, preencha e-mail e senha."
            messagebox.showwarning(*warning)
            return

        user = user_type.findByEmail(email)
        if not user:
            warning = "Atenção", "Email não encontrado"
            messagebox.showwarning(*warning)
            return

        if not user.checkPassword(password):
            warning = "Atenção", "Senha incorreta"
            messagebox.showwarning(*warning)
            return

        info = "Sucesso", "Login bem sucedido! Entrando na aplicação..."
        messagebox.showinfo(*info)
