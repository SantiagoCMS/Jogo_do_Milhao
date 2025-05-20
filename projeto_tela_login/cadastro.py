import customtkinter as ctk

from tkinter import messagebox

from database import Database

 

ctk.set_appearance_mode("light")

 

class CadastroApp(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent, fg_color="#f4ecda")

        self.title("Cadastro de Usuário")

        self.geometry("440x400")

        self.resizable(False, False)

 

        self.db = Database()

        self.criar_interface()

 

    def criar_interface(self):

        frame = ctk.CTkFrame(self, width=360, height=320, fg_color="#f4ecda", corner_radius=15)

        frame.pack(pady=30)

 

        ctk.CTkLabel(frame, text="Cadastro", font=("Century Gothic", 18, "bold"), text_color="#00A99D").pack(pady=(20, 10))

 

        self.entry_usuario = ctk.CTkEntry(

            frame, placeholder_text="Usuário", width=260, border_color="#003366", border_width=2

        )

        self.entry_usuario.pack(pady=10)

 

        self.entry_senha = ctk.CTkEntry(

            frame, placeholder_text="Senha", show="*", width=260, border_color="#ED1C24", border_width=2

        )

        self.entry_senha.pack(pady=10)

 

        ctk.CTkButton(

            frame,

            text="Cadastrar",

            fg_color="#F7931E",

            hover_color="#e68112",

            text_color="white",

            width=260,

            command=self.acao_cadastrar

        ).pack(pady=10)

 

        ctk.CTkButton(

            frame,

            text="Voltar para Login",

            fg_color="#F7931E",

            hover_color="#e68112",

            text_color="white",

            width=260,

            command=self.voltar_login

        ).pack(pady=(5, 10))

 

    def acao_cadastrar(self):

        usuario = self.entry_usuario.get()

        senha = self.entry_senha.get()

 

        if usuario and senha:

            sucesso = self.db.cadastrar_usuario(usuario, senha)

            if sucesso:

                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

                self.voltar_login()

            else:

                messagebox.showerror("Erro", "Usuário já existe.")

        else:

            messagebox.showerror("Erro", "Preencha todos os campos!")

 

    def voltar_login(self):

        self.destroy()