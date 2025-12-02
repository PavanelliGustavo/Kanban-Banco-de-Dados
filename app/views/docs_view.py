from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime

from app.models.model_corporate_user import Corporate
from app.models.model_document import Document
from app.models.model_public_work import PublicWork


class DocsViewFrame(tk.Frame):

    # region ---------------- VARIAVEIS (Mantidas) ----------------
    WINDOW_BACKGROUND_COLOR = "#f0f0f0"
    TEXT_FONT = "Helvetica"

    MAIN_CONTENT_PADDING = 40
    MAIN_CONTENT_PARAMS = {"bg": WINDOW_BACKGROUND_COLOR}
    MAIN_CONTENT_PACK_PARAMS = {"fill": "both",
                                "expand": True,
                                "padx": MAIN_CONTENT_PADDING,
                                "pady": MAIN_CONTENT_PADDING}
    # endregion

    # region ---------------- HEADER VARIABLES ----------------
    HEADER_FRAME_BG = "#f0f0f0"
    HEADER_FRAME_PACK_PADY = (0, 20)
    BACK_BUTTON_TEXT = "< Voltar"
    BACK_BUTTON_BG = "#ddd"
    BACK_BUTTON_PARAMS = {"bg": BACK_BUTTON_BG, "bd": 0, "padx": 10, "pady": 5}
    TITLE_TEXT = "Documentos"
    TITLE_PARAMS = {"font": (TEXT_FONT, 24, "bold"),
                    "bg": HEADER_FRAME_BG, "fg": "#333"}
    SUBTITLE_PARAMS = {"font": (TEXT_FONT, 10, "italic"),
                       "bg": HEADER_FRAME_BG, "fg": "#666"}
    # endregion

    # region ---------------- FILTER AREA VARIABLES ----------------
    FILTER_FRAME_BG = "#e0e0e0"
    FILTER_FRAME_PAD = 10
    FILTER_FRAME_PACK_PADY = (0, 10)
    FILTER_LABEL_TEXT = "Ordenar arquivos por:"
    COMBOBOX_VALUES = ["A-Z (Nome)", "Z-A (Nome)",
                       "Mais Recentes", "Mais Antigos"]
    APPLY_BUTTON_TEXT = "Aplicar Ordem"
    APPLY_BUTTON_BG = "#FF9800"
    APPLY_BUTTON_FG = "white"
    # endregion

    # region ---------------- LIST AREA VARIABLES ----------------
    TREE_COLUMNS = ("Documento", "Tipo", "Data")
    TREE_HEIGHT = 10
    COL_DOCUMENTO_WIDTH = 400
    COL_TIPO_WIDTH = 100
    COL_DATA_WIDTH = 150
    # endregion

    # region ---------------- ACTION BUTTON VARIABLES ----------------
    ACTION_BUTTON_TEXT = "ABRIR DOCUMENTO SELECIONADO"
    ACTION_BUTTON_BG = "#607D8B"
    ACTION_BUTTON_FG = "white"
    ACTION_BUTTON_FONT_STYLE = "bold"
    # endregion

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=self.WINDOW_BACKGROUND_COLOR)

        self.main_content = tk.Frame(self, **self.MAIN_CONTENT_PARAMS)
        self.main_content.pack(**self.MAIN_CONTENT_PACK_PARAMS)

        self.current_work_id = None
        self.current_work_name = None
        self.current_docs = []

    def update_view(self, work_id, work_name):
        self.current_work_id = int(work_id)
        self.current_work_name = work_name

        self.clearWidgets()
        self.createWidgets()
        self.loadInitialData()

    def clearWidgets(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def createWidgets(self):
        self.setUpHeader()
        self.setUpFilterArea()
        self.setUpDocumentList()
        self.setUpActionButton()

    def setUpHeader(self):
        header_frame = tk.Frame(self.main_content, bg=self.HEADER_FRAME_BG)
        header_frame.pack(fill="x", pady=self.HEADER_FRAME_PACK_PADY)

        def back_command():
            self.controller.show_kanban_frame(
                self.current_work_id, self.current_work_name)

        tk.Button(header_frame, text=self.BACK_BUTTON_TEXT, command=back_command,
                  **self.BACK_BUTTON_PARAMS).pack(side="left")

        tk.Label(header_frame, text=self.TITLE_TEXT, **
                 self.TITLE_PARAMS).pack(side="left", padx=30)

        subtitle_text = f"Referente a: {self.current_work_name}"
        tk.Label(header_frame, text=subtitle_text, **
                 self.SUBTITLE_PARAMS).pack(side="bottom", anchor="w")

    def setUpFilterArea(self):
        filter_frame = tk.Frame(self.main_content, bg=self.FILTER_FRAME_BG,
                                padx=self.FILTER_FRAME_PAD, pady=self.FILTER_FRAME_PAD)
        filter_frame.pack(fill="x", pady=self.FILTER_FRAME_PACK_PADY)

        # Container Esquerdo (Filtros + Pesquisa)
        left_area = tk.Frame(filter_frame, bg=self.FILTER_FRAME_BG)
        left_area.pack(side="left")

        # 1. Ordenação
        tk.Label(left_area, text=self.FILTER_LABEL_TEXT,
                 bg=self.FILTER_FRAME_BG).pack(side="left")

        self.combo_sort = ttk.Combobox(
            left_area, values=self.COMBOBOX_VALUES, width=20, state="readonly")
        self.combo_sort.current(2)
        self.combo_sort.pack(side="left", padx=5)

        tk.Button(left_area, text=self.APPLY_BUTTON_TEXT, command=self.apply_sort_and_search,
                  bg=self.APPLY_BUTTON_BG, fg=self.APPLY_BUTTON_FG).pack(side="left", padx=10)

        # 2. Pesquisa (IMPLEMENTAÇÃO NOVA)
        # Adicionado divisor visual
        tk.Label(left_area, text="|", bg=self.FILTER_FRAME_BG,
                 fg="#888").pack(side="left", padx=5)

        tk.Label(left_area, text="Pesquisar:",
                 bg=self.FILTER_FRAME_BG).pack(side="left", padx=5)
        self.entry_search = tk.Entry(left_area, width=25)
        self.entry_search.pack(side="left", padx=5)

        tk.Button(left_area, text="Buscar", command=self.apply_sort_and_search,
                  bg="#2196F3", fg="white").pack(side="left")

        # Container Direito (Botão Adicionar - Apenas Empresa)
        if self.controller.user_type == "empresa":
            tk.Button(filter_frame, text="Adicionar documentos",
                      command=lambda: self.open_document_modal(is_new=True),
                      bg="#2196F3", fg="white").pack(side="right", padx=10)

    def setUpDocumentList(self):
        tree_frame = tk.Frame(self.main_content)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            tree_frame, columns=self.TREE_COLUMNS, show="headings", height=self.TREE_HEIGHT)
        self.tree.heading("Documento", text="Nome do Arquivo")
        self.tree.heading("Tipo", text="Formato")
        self.tree.heading("Data", text="Data de Publicação")

        self.tree.column("Documento", width=self.COL_DOCUMENTO_WIDTH)
        self.tree.column("Tipo", width=self.COL_TIPO_WIDTH, anchor="center")
        self.tree.column("Data", width=self.COL_DATA_WIDTH, anchor="center")

        self.tree.pack(fill="both", expand=True, side="left")

        sb = ttk.Scrollbar(tree_frame, orient="vertical",
                           command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.bind("<Double-1>", self.on_open_document)

    def setUpActionButton(self):
        tk.Button(self.main_content, text=self.ACTION_BUTTON_TEXT,
                  command=self.on_open_document,
                  bg=self.ACTION_BUTTON_BG, fg=self.ACTION_BUTTON_FG,
                  font=(self.TEXT_FONT, 10, "bold"), pady=10).pack(fill="x", pady=20)

    def loadInitialData(self):
        documents: list[Document] = Document.listAll()
        if documents:
            self.current_docs = [
                d for d in documents if d.getPublicWorkId() == int(self.current_work_id)]
        else:
            self.current_docs = []
        self.apply_sort_and_search()

    def populate_tree(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not data:
            self.tree.insert("", "end", values=(
                "Nenhum documento encontrado.", "-", "-"))
        else:
            for doc in data:
                self.tree.insert("", "end", iid=doc['id'], values=(
                    doc['titulo'], doc['tipo'], doc['data']))

    def apply_sort_and_search(self):
        # 1. Cópia dos dados
        data: list[Document] = self.current_docs[:]

        # 2. Pesquisa
        if hasattr(self, 'entry_search'):
            term = self.entry_search.get().lower().strip()
            if term:
                data = [d for d in data if term in d.getTitle().lower()]

        # 3. Ordenação
        sort_opt = self.combo_sort.get()
        if sort_opt == "A-Z (Nome)":
            data.sort(key=lambda x: x.getTitle())
        elif sort_opt == "Z-A (Nome)":
            data.sort(key=lambda x: x.getTitle(), reverse=True)
        elif sort_opt == "Mais Recentes":
            data.sort(key=lambda x: x.getUploadDate(), reverse=True)
        elif sort_opt == "Mais Antigos":
            data.sort(key=lambda x: x.getUploadDate())

        self.populate_tree(data)

    def on_open_document(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um documento.")
            return

        doc_id = int(selected[0])
        doc_data = next(
            (d for d in Document.listAll() if d.getId() == doc_id), None)
        if not doc_data:
            return

        if self.controller.user_type == "empresa":
            self.open_file_options_modal(doc_data)
        else:
            self.simulate_open_file(doc_data)

    def simulate_open_file(self, doc_data):
        messagebox.showinfo(
            "Abrir Arquivo", f"O arquivo '{doc_data['titulo']}' seria aberto agora.")

    def open_file_options_modal(self, doc_data):
        options_window = tk.Toplevel(self)
        options_window.title("Opções")
        options_window.geometry("300x250")
        options_window.configure(bg="white")
        options_window.grab_set()

        tk.Label(options_window, text="O que deseja fazer?", font=(
            "Helvetica", 12, "bold"), bg="white").pack(pady=20)

        # Abrir (Verde)
        tk.Button(options_window, text="ABRIR", bg="#4CAF50", fg="white", font=("bold"), width=20,
                  command=lambda: [options_window.destroy(), self.simulate_open_file(doc_data)]).pack(pady=5)

        # Editar (Laranja)
        tk.Button(options_window, text="EDITAR", bg="#FF9800", fg="white", font=("bold"), width=20,
                  command=lambda: [options_window.destroy(), self.open_document_modal(is_new=False, doc_data=doc_data)]).pack(pady=5)

        # Excluir (Vermelho)
        tk.Button(options_window, text="EXCLUIR", bg="#f44336", fg="white", font=("bold"), width=20,
                  command=lambda: self.confirm_delete_popup(options_window, doc_data)).pack(pady=5)

    def confirm_delete_popup(self, parent_modal, doc_data):
        popup = tk.Toplevel(self)
        popup.title("Confirmação")
        popup.geometry("350x150")
        popup.configure(bg="white")
        popup.grab_set()

        tk.Label(popup, text="Deseja excluir o documento?",
                 font=("Helvetica", 12), bg="white").pack(pady=25)
        btn_frame = tk.Frame(popup, bg="white")
        btn_frame.pack()

        tk.Button(btn_frame, text="SIM", bg="#4CAF50", fg="white", width=10, font=("bold"),
                  command=lambda: self.perform_delete(doc_data, popup, parent_modal)).pack(side="left", padx=15)

        tk.Button(btn_frame, text="NÃO", bg="#f44336", fg="white", width=10, font=("bold"),
                  command=popup.destroy).pack(side="right", padx=15)

    def perform_delete(self, doc_data, popup, parent_modal):
        doc_data.delete()
        popup.destroy()
        parent_modal.destroy()
        self.loadInitialData()
        messagebox.showinfo("Sucesso", "Documento excluído.")

    def open_document_modal(self, is_new, doc_data=None):
        modal = tk.Toplevel(self)
        title = "Adicionar Documento" if is_new else "Editar Documento"
        modal.title(title)
        modal.geometry("400x350")
        modal.configure(bg="white")
        modal.grab_set()

        tk.Label(modal, text=title, font=("Helvetica", 14, "bold"),
                 bg="white", fg="#2196F3").pack(pady=20)

        # Nome
        tk.Label(modal, text="Nome de Exibição:", font=("bold", 10),
                 bg="white", anchor="w").pack(fill="x", padx=30, pady=(5, 0))
        entry_name = tk.Entry(modal, bg="#fafafa")
        entry_name.pack(fill="x", padx=30, pady=(0, 10))

        # Arquivo
        tk.Label(modal, text="Arquivo PDF:", font=("bold", 10),
                 bg="white", anchor="w").pack(fill="x", padx=30, pady=(5, 0))
        file_frame = tk.Frame(modal, bg="white")
        file_frame.pack(fill="x", padx=30)

        entry_path = tk.Entry(file_frame, bg="#fafafa", state="readonly")
        entry_path.pack(side="left", fill="x", expand=True)

        def select_file():
            filename = filedialog.askopenfilename(
                filetypes=[("PDF Files", "*.pdf")])
            if filename:
                entry_path.configure(state="normal")
                entry_path.delete(0, "end")
                entry_path.insert(0, filename)
                entry_path.configure(state="readonly")

        tk.Button(file_frame, text="...", command=select_file,
                  width=3).pack(side="left", padx=(5, 0))

        if not is_new and doc_data:
            entry_name.insert(0, doc_data['titulo'])
            entry_path.configure(state="normal")
            entry_path.insert(0, doc_data['caminho'])
            entry_path.configure(state="readonly")

        tk.Button(modal, text="Salvar mudanças", bg="#4CAF50", fg="white", font=("bold"), pady=8,
                  command=lambda: self.confirm_save_popup(modal, entry_name, entry_path, is_new, doc_data)).pack(pady=30)

    def confirm_save_popup(self, parent_modal, entry_name, entry_path, is_new, doc_data):
        name = entry_name.get().strip()
        path = entry_path.get().strip()

        if not name:
            messagebox.showwarning(
                "Erro", "O arquivo inserido precisa ter um Nome", parent=parent_modal)
            return

        if not path:
            messagebox.showwarning(
                "Erro", "Arquivo não foi adicionado", parent=parent_modal)
            return

        if not path.lower().endswith('.pdf'):
            messagebox.showwarning(
                "Erro", "Arquivo precisa estar em formato PDF", parent=parent_modal)
            return

        popup = tk.Toplevel(self)
        popup.title("Confirmação")
        popup.geometry("350x150")
        popup.configure(bg="white")
        popup.grab_set()

        try:
            x = parent_modal.winfo_rootx() + 25
            y = parent_modal.winfo_rooty() + 100
            popup.geometry(f"+{x}+{y}")
        except:
            pass

        tk.Label(popup, text="Deseja salvar as mudanças?",
                 font=("Helvetica", 12), bg="white").pack(pady=25)
        btn_frame = tk.Frame(popup, bg="white")
        btn_frame.pack()

        tk.Button(btn_frame, text="SIM", bg="#4CAF50", fg="white", width=10, font=("bold"),
                  command=lambda: self.perform_save(is_new, doc_data, name, path, popup, parent_modal)).pack(side="left", padx=15)

        tk.Button(btn_frame, text="NÃO", bg="#f44336", fg="white", width=10, font=("bold"),
                  command=popup.destroy).pack(side="right", padx=15)

    def perform_save(self, is_new, doc_data: Document, name, path, popup, parent_modal):

        with open(Path(path), "rb") as file:
            content = file.read()

        if is_new:
            pw: PublicWork = PublicWork.getById(self.current_work_id)
            corp: Corporate = Corporate.getById(pw.getCorporateId())

            doc = Document(name, content, pw.getId(), 1, corp.getId())
            doc.setUploadDate()
            doc.pushDatabase()
        else:
            doc_data.setTitle(name)
            doc_data.setUploadDate()
            doc_data.setFileData(content)
            doc_data.pushDatabase()

        popup.destroy()
        parent_modal.destroy()
        self.loadInitialData()
        messagebox.showinfo("Sucesso", "Mudanças salvas com sucesso!")
