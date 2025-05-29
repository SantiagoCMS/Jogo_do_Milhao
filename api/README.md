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


## IMPORTANTE

2- Comando de teste para rodar API: uvicorn api.main:app --reload


## 🚀 Como rodar localmente

1. **Clone o repositório:**

git clone https://github.com/seu-usuario/seu-repo.git

2. **Criar e editar arquivo .env:**

Ver modelo de arquivo .env em .env.example

3. **Install das bibliotecas:**

Instalar as bibliotecas necessarias rodando comando: pip install -r requirements.txt