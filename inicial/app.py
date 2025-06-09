import customtkinter as ctk
from PIL import Image
import os
import json
from jogo.game import Game
import sqlite3

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Jogo do Milhão - Login")
        self.geometry("700x650")
        self.resizable(False, False)
        self.fg_color = "#F5F5DC"
        self.configure(fg_color=self.fg_color)
        self.criar_interface()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.usuarios_path = os.path.join(base_dir, "usuarios.json")

        if not os.path.exists(self.usuarios_path):
            with open(self.usuarios_path, "w") as f:
                json.dump({}, f)

    def criar_interface(self):
        frame = ctk.CTkFrame(self, fg_color=self.fg_color)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "imagens", "Poliedro.png")
        imagem_ctk = ctk.CTkImage(light_image=Image.open(img_path), size=(180, 180))
        label_imagem = ctk.CTkLabel(frame, image=imagem_ctk, text="")
        label_imagem.pack(pady=(0, 20))

        # Frame usuário
        usuario_frame = ctk.CTkFrame(frame, fg_color=self.fg_color)
        usuario_frame.pack(fill="x", pady=(0, 15))

        label_usuario = ctk.CTkLabel(usuario_frame, text="Usuário", text_color="#F7931E")
        label_usuario.pack(anchor="w", padx=2, pady=(0, 3))

        self.entry_usuario = ctk.CTkEntry(usuario_frame, width=500, fg_color="white", text_color="black")
        self.entry_usuario.pack(fill="x")

        # Frame senha
        senha_frame = ctk.CTkFrame(frame, fg_color=self.fg_color)
        senha_frame.pack(fill="x", pady=(0, 20))

        label_senha = ctk.CTkLabel(senha_frame, text="Senha", text_color="#F7931E")
        label_senha.pack(anchor="w", padx=2, pady=(0, 3))

        self.entry_senha = ctk.CTkEntry(senha_frame, width=500, show="*", fg_color="white", text_color="black")
        self.entry_senha.pack(fill="x")

        # Label para mensagens de erro/sucesso
        self.label_mensagem = ctk.CTkLabel(frame, text="", text_color="red", font=ctk.CTkFont(size=14))
        self.label_mensagem.pack(pady=(0, 10))

        login_button = ctk.CTkButton(frame, text="Login", width=500, command=self.login, font=ctk.CTkFont(size=16))
        login_button.pack(pady=(0, 10))

        cadastro_button = ctk.CTkButton(
            frame, text="Cadastrar",
            width=500,
            fg_color="#F7931E",
            hover_color="#e68112",
            text_color="black",
            font=ctk.CTkFont(size=16),
            command=self.abrir_cadastro
        )
        cadastro_button.pack()

    def login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            self.label_mensagem.configure(text="Preencha usuário e senha.", text_color="red")
            return

        with open(self.usuarios_path, "r") as f:
            usuarios = json.load(f)

        if usuario in usuarios and usuarios[usuario] == senha:
            self.label_mensagem.configure(text=f"Login bem-sucedido, {usuario}!", text_color="green")
            self.abrir_jogo(usuario)
        else:
            self.label_mensagem.configure(text="Usuário ou senha inválidos!", text_color="red")

    def abrir_jogo(self, usuario):
        self.withdraw()
        jogo = Game()
        jogo.run()
        self.deiconify()

    def abrir_cadastro(self):
        janela_cadastro = ctk.CTkToplevel(self)
        janela_cadastro.title("Cadastro de Usuário")
        janela_cadastro.geometry("600x550")
        janela_cadastro.resizable(False, False)
        janela_cadastro.configure(fg_color=self.fg_color)

        label_info = ctk.CTkLabel(
            janela_cadastro,
            text="Cadastro do Aluno",
            fg_color=self.fg_color,
            font=ctk.CTkFont(size=18),
            text_color="#F7931E"  # Laranja
        )
        label_info.pack(pady=20)

        # Frame novo usuário
        usuario_frame = ctk.CTkFrame(janela_cadastro, fg_color=self.fg_color)
        usuario_frame.pack(fill="x", pady=(0, 15), padx=20)

        label_novo_usuario = ctk.CTkLabel(usuario_frame, text="Usuário", text_color="#F7931E")
        label_novo_usuario.pack(anchor="w", pady=(0, 3))

        entry_novo_usuario = ctk.CTkEntry(usuario_frame, width=500, fg_color="white", text_color="black")
        entry_novo_usuario.pack(fill="x")

        # Frame nova senha
        senha_frame = ctk.CTkFrame(janela_cadastro, fg_color=self.fg_color)
        senha_frame.pack(fill="x", pady=(0, 20), padx=20)

        label_nova_senha = ctk.CTkLabel(senha_frame, text="Senha", text_color="#F7931E")
        label_nova_senha.pack(anchor="w", pady=(0, 3))

        entry_nova_senha = ctk.CTkEntry(senha_frame, width=500, show="*", fg_color="white", text_color="black")
        entry_nova_senha.pack(fill="x")

        # Label para mensagens na janela cadastro
        label_mensagem_cadastro = ctk.CTkLabel(janela_cadastro, text="", text_color="red", font=ctk.CTkFont(size=14))
        label_mensagem_cadastro.pack(pady=(0, 10))

        def salvar_cadastro():
            novo_usuario = entry_novo_usuario.get().strip()
            nova_senha = entry_nova_senha.get().strip()

            if not novo_usuario or not nova_senha:
                label_mensagem_cadastro.configure(text="Usuário e senha não podem ser vazios.", text_color="red")
                return

            with open(self.usuarios_path, "r") as f:
                usuarios = json.load(f)

            if novo_usuario in usuarios:
                label_mensagem_cadastro.configure(text="Usuário já existe!", text_color="red")
                return

            usuarios[novo_usuario] = nova_senha

            with open(self.usuarios_path, "w") as f:
                json.dump(usuarios, f, indent=4)

            label_mensagem_cadastro.configure(text=f"Usuário {novo_usuario} cadastrado com sucesso!", text_color="green")
            janela_cadastro.after(1500, janela_cadastro.destroy)

        salvar_button = ctk.CTkButton(
            janela_cadastro,
            text="Salvar",
            width=500,
            font=ctk.CTkFont(size=16),
            command=salvar_cadastro
            # Sem fg_color e text_color para ficar igual ao botão Login
        )
        salvar_button.pack(pady=10, padx=20)

        fechar_button = ctk.CTkButton(
            janela_cadastro,
            text="Voltar",
            width=500,
            font=ctk.CTkFont(size=16),
            command=janela_cadastro.destroy,
            fg_color="#F7931E",
            hover_color="#e68112",
            text_color="black"
        )
        fechar_button.pack(pady=10, padx=20)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = LoginApp()
    app.mainloop()
