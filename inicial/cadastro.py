import customtkinter as ctk
from PIL import Image
import os
import json

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Jogo do Milhão - Login")
        self.geometry("500x550")
        self.resizable(False, False)
        self.fg_color = "#F5F5DC"
        self.configure(fg_color=self.fg_color)
        self.criar_interface()

        # Caminho do arquivo de usuários
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.usuarios_path = os.path.join(base_dir, "usuarios.json")

        # Se não existir, cria arquivo vazio
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

        label_usuario = ctk.CTkLabel(frame, text="Usuário", fg_color=self.fg_color)
        label_usuario.pack(anchor="w")
        self.entry_usuario = ctk.CTkEntry(frame, width=350)
        self.entry_usuario.pack(pady=(0, 15))

        label_senha = ctk.CTkLabel(frame, text="Senha", fg_color=self.fg_color)
        label_senha.pack(anchor="w")
        self.entry_senha = ctk.CTkEntry(frame, width=350, show="*")
        self.entry_senha.pack(pady=(0, 20))

        login_button = ctk.CTkButton(frame, text="Login", width=350, command=self.login)
        login_button.pack(pady=(0, 10))

        cadastro_button = ctk.CTkButton(
            frame, text="Cadastrar",
            width=350,
            fg_color="#F7931E",
            hover_color="#e68112",
            text_color="white",
            command=self.abrir_cadastro
        )
        cadastro_button.pack()

    def login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        print(f"Tentando login com usuário: {usuario} e senha: {senha}")
        # Aqui coloca sua lógica de autenticação real

    def abrir_cadastro(self):
        janela_cadastro = ctk.CTkToplevel(self)
        janela_cadastro.title("Cadastro de Usuário")
        janela_cadastro.geometry("450x400")
        janela_cadastro.resizable(False, False)
        janela_cadastro.configure(fg_color=self.fg_color)

        label_info = ctk.CTkLabel(janela_cadastro, text="Preencha os dados para cadastro", fg_color=self.fg_color)
        label_info.pack(pady=20)

        label_novo_usuario = ctk.CTkLabel(janela_cadastro, text="Novo Usuário", fg_color=self.fg_color)
        label_novo_usuario.pack(anchor="w", padx=20)
        entry_novo_usuario = ctk.CTkEntry(janela_cadastro, width=350)
        entry_novo_usuario.pack(pady=(0, 15), padx=20)

        label_nova_senha = ctk.CTkLabel(janela_cadastro, text="Nova Senha", fg_color=self.fg_color)
        label_nova_senha.pack(anchor="w", padx=20)
        entry_nova_senha = ctk.CTkEntry(janela_cadastro, width=350, show="*")
        entry_nova_senha.pack(pady=(0, 20), padx=20)

        def salvar_cadastro():
            novo_usuario = entry_novo_usuario.get().strip()
            nova_senha = entry_nova_senha.get().strip()

            if not novo_usuario or not nova_senha:
                print("Usuário e senha não podem ser vazios.")
                return

            # Carrega usuários existentes
            with open(self.usuarios_path, "r") as f:
                usuarios = json.load(f)

            if novo_usuario in usuarios:
                print("Usuário já existe!")
                return

            # Salva novo usuário
            usuarios[novo_usuario] = nova_senha

            with open(self.usuarios_path, "w") as f:
                json.dump(usuarios, f, indent=4)

            print(f"Usuário {novo_usuario} cadastrado com sucesso!")
            janela_cadastro.destroy()

        salvar_button = ctk.CTkButton(janela_cadastro, text="Salvar", width=350, command=salvar_cadastro)
        salvar_button.pack(pady=10, padx=20)

        fechar_button = ctk.CTkButton(janela_cadastro, text="Cancelar", width=350, command=janela_cadastro.destroy)
        fechar_button.pack(pady=10, padx=20)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = LoginApp()
    app.mainloop()
