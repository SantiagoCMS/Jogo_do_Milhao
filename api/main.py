from fastapi import FastAPI
from .database import engine, Base
from .routes import router, registar_todas_rotas

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI(
    title = "Mente Milionária - Quiz Game",
    description = "API para gerenciamento do jogo de perguntas e respostas Mente Milionária",
    version = "1.0.0",
)

# Registra as rotas encapsuladas nas classes
registar_todas_rotas()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Mente Milionária! Para acessar a documentação, visite /docs ou /redoc."}

# Inclui o router no app principal
app.include_router(router)