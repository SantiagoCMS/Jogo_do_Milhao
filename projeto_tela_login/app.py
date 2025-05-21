import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
from projeto_tela_login.database import Database
from projeto_tela_login.cadastro import CadastroApp
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#F4E4C4")  # Cor do fundo alterada
        self.title("Sistema de Login")
        self.geometry("800x500")
        self.resizable(False, False)

        self.db = Database()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.criar_interface()

    def criar_interface(self):
        caminho_base = os.path.dirname(os.path.abspath(__file__))
        caminho_imagem = os.path.join(caminho_base, "imagens", "Poliedro.png")

        imagem_original = Image.open(caminho_imagem).resize((300, 300))
        self.img = ImageTk.PhotoImage(imagem_original)

        self.lb_img = ctk.CTkLabel(self, text="", image=self.img)
        self.lb_img.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        frame_login = ctk.CTkFrame(self, width=340, height=360, fg_color="#F4E4C4", corner_radius=15)
        frame_login.grid(row=0, column=1, padx=40, pady=40, sticky="n")

        title_label = ctk.CTkLabel(frame_login, text="Sign in", font=("Century Gothic", 18, "bold"), text_color="#00A99D")
        title_label.pack(pady=(20, 10))

        self.entry_usuario = ctk.CTkEntry(frame_login, placeholder_text="Usuário", width=260, border_color="#003366", border_width=2)
        self.entry_usuario.pack(pady=10)

        self.entry_senha = ctk.CTkEntry(frame_login, placeholder_text="Senha", show="*", width=260, border_color="#ED1C24", border_width=2)
        self.entry_senha.pack(pady=10)

        login_button = ctk.CTkButton(frame_login, text="Entrar", fg_color="#F7931E", hover_color="#e68112", text_color="white", width=260, command=self.acao_login)
        login_button.pack(pady=(15, 10))

        cadastro_button = ctk.CTkButton(frame_login, text="Cadastrar", fg_color="#F7931E", hover_color="#e68112", text_color="white", width=260, command=self.abrir_cadastro)
        cadastro_button.pack(pady=(0, 10))

    def acao_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if self.db.verificar_login(usuario, senha):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def abrir_cadastro(self):
        CadastroApp(self)

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
