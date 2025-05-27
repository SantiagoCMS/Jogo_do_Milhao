from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexão com o banco de dados propriamente dita a partir da URL
DATABASE_URL = "mysql+pymysql://avnadmin:SENHA_DB@mentemilionaria-santiago-6fa1.h.aivencloud.com:14266/defaultdb?ssl_ca=./ca-cert.pem"

# "Engine" gerencia conexões com o banco de dados
engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {"verify_cert": True}}  # Força validação do certificado "ca-cert.pem"
)

# "SessionLocal" é uma classe que cria sessões locais e temporarias para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma função de dependência para injeção de sessão no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# "Base" é a classe base para os modelos do banco de dados
Base = declarative_base()

# Teste de conexão com o banco de dados

# from sqlalchemy import text
# try:
#     with engine.connect() as conn:
#         conn.execute(text("SELECT 1"))  # Query simples de teste
#     print("✅ Conexão bem-sucedida!")
# except Exception as e:
#     print(f"❌ Falha na conexão: {e}")