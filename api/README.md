# 📂 Estrutura da API - MenteMilionária


## 🗃️ Arquivos Existentes

### 1. `database.py`
**Função**: Configuração da conexão com o banco de dados MySQL (Aiven).  

### 2. `models.py`
**Função**: Define as tabelas do banco como classes Python

### 3. `schemas.py`
**Função**: Valida dados de entrada e saída da API usando Pydantic

### 4. `crud.py`
**Função**: Faz todas as operações do BD, como criar entidades (usuários, turmas, matérias
questões) ou fazer consultas especificas (buscar questoes por materia e nivel etc.)

### 5. `routes.py`
**Função**: Define os endpoints da API

### 6. `main.py`
**Função**: Ponto de entrada da API, configuração do FastAPI

## Installs Necessários

1- pip install sqlalchemy
2- pip install fastapi

## IMPORTANTE

1- Para o funcionamento da API e a conexão correta com o BD insira a senha real 
na URL do arquivo database.py

2- Comando de teste para rodar API: uvicorn api.main:app --reload