import mysql.connector
from mysql.connector import Error
from tela_Login_Inicial.credenciais import host, user, database, password

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor()
            self.criar_tabela()
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def criar_tabela(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                )
            ''')
            self.connection.commit()

            self.cursor.execute('SELECT * FROM usuarios WHERE username = %s', ("Usuarioprof",))
            if self.cursor.fetchone() is None:
                self.cursor.execute('INSERT INTO usuarios (username, password) VALUES (%s, %s)', ("Usuarioprof", "senhaprof"))
                self.connection.commit()
                print("Usuário padrão 'Usuarioprof' inserido.")
            else:
                print("Usuário padrão já existe.")
        except Error as e:
            print(f"Erro ao criar tabela ou inserir usuário padrão: {e}")

    def verificar_login(self, username, password):
        try:
            self.cursor.execute('SELECT * FROM usuarios WHERE username = %s AND password = %s', (username, password))
            return self.cursor.fetchone() is not None
        except Error as e:
            print(f"Erro ao verificar login: {e}")
            return False

    def cadastrar_usuario(self, username, password):
        try:
            self.cursor.execute('INSERT INTO usuarios (username, password) VALUES (%s, %s)', (username, password))
            self.connection.commit()
            return True
        except mysql.connector.IntegrityError:
            return False
        except Error as e:
            print(f"Erro ao cadastrar usuário: {e}")
            return False

    def fechar(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
