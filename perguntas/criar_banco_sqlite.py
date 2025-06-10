import sqlite3
import json
import os

# Caminho para o diretório onde este script está
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) # Assume que o script está em 'gerenciamento_perguntas/'

# O arquivo JSON está na mesma pasta que este script
JSON_FILENAME = os.path.join(SCRIPT_DIR, "perguntas.json")

# Caminho para a pasta 'jogo/' que está um nível acima e depois dentro de 'jogo'
# (SeuProjetoQuiz/jogo/quiz_banco.db)
PROJECT_ROOT_DIR = os.path.dirname(SCRIPT_DIR)
JOGO_DIR = os.path.join(PROJECT_ROOT_DIR, "jogo")
SQLITE_DB_FILENAME = os.path.join(JOGO_DIR, "quiz_banco.db")

def criar_ou_atualizar_banco():
    conn = None
    try:
        # Garante que a pasta 'jogo' existe para salvar o .db (caso não tenha rodado o jogo ainda)
        os.makedirs(JOGO_DIR, exist_ok=True)

        print(f"Conectando/Criando banco de dados em: {SQLITE_DB_FILENAME}")
        conn = sqlite3.connect(SQLITE_DB_FILENAME)
        cursor = conn.cursor()


        # Verifica se a tabela "questions" existe e cria se não existir
        print("Criando tabela 'questions' se não existir...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            answer_a TEXT,
            answer_b TEXT,
            answer_c TEXT,
            answer_d TEXT,
            correct_answer TEXT NOT NULL,
            tip TEXT,
            subject TEXT,
            level TEXT
        )
        """)
        conn.commit()
        print("Tabela 'questions' verificada/criada.")


        # Verifica se a tabela "usuários" existe e cria se não existir
        print("Cirando tabela 'usuarios' se não existir...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """)
        conn.commit()
        print("Tabela 'usuarios' verificada/criada.")


        # Verifica se a tabela "ranking" existe e cria se não existir
        print("Criando tabela 'ranking' se não existir...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT NOT NULL,
            score INTEGER,
            FOREIGN KEY (user_id) REFERENCES usuarios (id)
        )
        """)
        conn.commit()
        print("Tabela 'ranking' verificada/criada.")


        # >>>>> MODIFICAÇÃO AQUI: Limpa as tabelas antes de inserir <<<<<
        print("Limpando perguntas existentes da tabela 'questions' para atualização...")
        cursor.execute("DELETE FROM questions")
        conn.commit()
        print("Tabela 'questions' limpa.")

        print("Limpando usuários existentes da tabela 'usuarios' para atualização...")
        cursor.execute("DELETE FROM usuarios")
        conn.commit()
        print("Tabela 'usuarios' limpa.")

        print("Limpando ranking existente da tabela 'ranking' para atualização...")
        cursor.execute("DELETE FROM ranking")
        conn.commit()
        print("Tabela 'ranking' limpa.")
        # >>>>> FIM DA MODIFICAÇÃO <<<<<

        print(f"Carregando perguntas do arquivo: {JSON_FILENAME}")
        try:
            with open(JSON_FILENAME, 'r', encoding='utf-8') as f:
                perguntas_data = json.load(f)
        except FileNotFoundError:
            print(f"ERRO: Arquivo '{JSON_FILENAME}' não encontrado. Nenhuma pergunta será adicionada.")
            return # Sai se o JSON não for encontrado
        except json.JSONDecodeError:
            print(f"ERRO: Falha ao decodificar JSON do arquivo '{JSON_FILENAME}'. Verifique o formato.")
            return
        except Exception as e:
            print(f"ERRO ao ler {JSON_FILENAME}: {e}")
            return

        if not perguntas_data:
            print(f"Nenhum dado encontrado em '{JSON_FILENAME}'. O banco de dados não será populado.")
            return

        print(f"{len(perguntas_data)} perguntas carregadas do JSON. Iniciando inserção no SQLite...")
        perguntas_inseridas_count = 0
        for p_idx, p in enumerate(perguntas_data):
            try:
                if not isinstance(p, dict) or \
                   not all(k in p for k in ['text', 'answers', 'correct_answer', 'tip', 'subject', 'level']) or \
                   not isinstance(p['answers'], dict) or \
                   not all(ak in p['answers'] for ak in ['A', 'B', 'C', 'D']):
                    print(f"AVISO (Pergunta {p_idx+1}): Estrutura inválida ou faltando chaves. Não será inserida: {p.get('text', 'Texto desconhecido')[:50]}...")
                    continue

                cursor.execute("""
                    INSERT INTO questions (text, answer_a, answer_b, answer_c, answer_d, correct_answer, tip, subject, level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    p['text'], p['answers'].get('A'), p['answers'].get('B'),
                    p['answers'].get('C'), p['answers'].get('D'),
                    p['correct_answer'], p['tip'], p['subject'], p['level']
                ))
                perguntas_inseridas_count += 1
            except Exception as e:
                print(f"Erro ao inserir pergunta {p_idx+1} ('{p.get('text', 'Texto desconhecido')[:50]}...'): {e}")

        conn.commit()
        if perguntas_inseridas_count > 0:
            print(f"{perguntas_inseridas_count} perguntas foram inseridas/atualizadas no banco '{SQLITE_DB_FILENAME}'.")
        else:
            print("Nenhuma pergunta nova foi inserida no banco de dados (verifique avisos ou o arquivo JSON).")

    except sqlite3.Error as e:
        print(f"Erro geral com SQLite: {e}")
        if conn:
            conn.rollback() # Reverte alterações se um erro de SQL ocorrer durante transações maiores
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        if conn:
            conn.close()
            print(f"Conexão com '{SQLITE_DB_FILENAME}' fechada.")

if __name__ == "__main__":
    criar_ou_atualizar_banco()