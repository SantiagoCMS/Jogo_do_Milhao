from pydantic import BaseModel, Field
from typing import Optional, List

# ----MODELOS PYDANTIC PARA VALIDAÇÃO DE DADOS NA API----
# 
# Estrutura padrão para cada entidade:
# 1. ClasseBase: Campos comuns para criação/consulta
# 2. ClasseCreate: Herda Base + campos obrigatórios para criação
# 3. ClasseResponse: Herda Base + campos de resposta + orm_mode

# ----USUÁRIO----

class UsuarioBase(BaseModel):
    nomeUsuario: str = Field(..., max_length=60)    # Campos básicos compartilhados entre criação e resposta
    senhaUsuario: str = Field(..., max_length=45)

class UsuarioCreate(UsuarioBase):
    idUsuario: str = Field(..., max_length=15)    # Dados necessários para criar um usuário (POST)

class UsuarioResponse(UsuarioBase):    # Dados retornados ao consultar usuário (GET) - omite a senha por segurança
    idUsuario: str

class UsuarioLogin(BaseModel):    # Dados necessários para login (POST)
    nomeUsuario: str = Field(..., max_length=60)    # Nome de usuário

    class Config:
        from_attributes = True    # Permite conversão automática de modelos SQLAlchemy → Pydantic


# ----TIPO DE USUÁRIO----

class TipoUsuarioBase(BaseModel):
    tipoUsuario: str = Field(..., max_length=15)    # Tipos de usuário (professor ou aluno)

class TipoUsuarioCreate(TipoUsuarioBase):    # Criação com ID (gerado automaticamente no banco)
    idTipo_Usuario: int

class TipoUsuarioResponse(TipoUsuarioBase):    # Resposta retornada inclui ID do tipo de usuário
    idTipo_Usuario: int

    class Config:
        from_attributes = True


# ----TURMA----

class TurmaBase(BaseModel):    # Turmas dos usuários (E.M. ou E.F.)
    nomeTurma: str

class TurmaCreate(TurmaBase):    # Criação com código da turma (ID)
    codigoTurma: int

class TurmaResponse(TurmaBase):    # Resposta inclui código
    codigoTurma: int

    class Config:
        from_attributes = True


# ----CADASTRO----

class CadastroBase(BaseModel):    # Relaciona Usuário-Tipo-Turma
    Usuario_idUsuario: str # Chave estrangeira
    Tipo_Usuario_idTipo_Usuario: int # Chave estrangeira
    Turma_codigoTurma: int # Chave estrangeira

class CadastroCreate(CadastroBase): # Para criação (mesmos campos que Base)
    pass

class CadastroResponse(CadastroBase):
    class Config:
        from_attributes = True


# ----MATÉRIA----

class MateriaBase(BaseModel):    # Matérias do jogo (Matemática, História...)
    nomeMateria: str

class MateriaCreate(MateriaBase):    # Criação com ID da matéria (gerado automaticamente no banco)
    idMateria: int

class MateriaResponse(MateriaBase):    # Resposta inclui ID da matéria
    idMateria: int

    class Config:
        from_attributes = True


# ----NÍVEL----

class NivelBase(BaseModel):    # Níveis de dificuldade (Fácil, Médio, Difícil)
    descricaoNivel: str

class NivelCreate(NivelBase):    # Criação com ID do nível (gerado automaticamente no banco)
    idNivel: int

class NivelResponse(NivelBase):    # Resposta inclui ID do nível
    idNivel: int

    class Config:
        from_attributes = True


# ----TIPO DE AJUDA----

class TipoAjudaBase(BaseModel):    # Tipos de ajuda (eliminação, pular e dicas)
    nomeAjuda: str

class TipoAjudaCreate(TipoAjudaBase):    # Criação com código da ajuda (ID)
    codAjuda: int

class TipoAjudaResponse(TipoAjudaBase):    # Resposta inclui código da ajuda
    codAjuda: int

    class Config:
        from_attributes = True


# ----PONTUAÇÃO----

class PontuacaoBase(BaseModel):    # Registro de pontuação dos usuários
    pontuacao: int                 # Pontuação do usuário
    Usuario_idUsuario: str         # Chave estrangeira
    Materia_idMateria: int         # Chave estrangeira
    Nivel_idNivel: int             # Chave estrangeira

class PontuacaoCreate(PontuacaoBase):    # Para criação de pontuação (mesmos campos que Base)
    pass

class PontuacaoResponse(PontuacaoBase):
    class Config:
        from_attributes = True


# ----QUESTÃO----

class QuestaoBase(BaseModel):    # Questões do jogo (com alternativas)
    Enunciado: str                          # Enunciado da questão
    respostaCorreta: str                    # Resposta correta
    AlternativaA: str                       # A
    AlternativaB: str                       # B
    AlternativaC: str                       # C
    AlternativaD: str                       # D

class QuestaoCreate(QuestaoBase):    # Criação de questão com ID (gerado automaticamente no banco)
    idQuestaoAlternativa: int

class QuestaoResponse(QuestaoBase):    # Resposta inclui ID da questão
    idQuestao: int

    class Config:
        from_attributes = True

# ----SELECIONAR JOGO----

class SelecionarJogoBase(BaseModel):
    Cadastro_Usuario_idUsuario: str                  # Chave estrangeira para usuário      
    Cadastro_Tipo_Usuario_idTipo_Usuario: int        # Chave estrangeira
    Cadastro_Turma_codigoTurma: int                  # Chave estrangeira 
    Materia_idMateria: int                           # Chave estrangeira
    Questao_idQuestao: int    # Chave estrangeira
    TipoAjuda_codAjuda: int                          # Chave estrangeira
    Nivel_idNivel: int                               # Chave estrangeira   

class SelecionarJogoCreate(SelecionarJogoBase):    # Para criação de seleção de jogo (mesmos campos que Base)
    pass

class SelecionarJogoResponse(SelecionarJogoBase):
    class Config:
        from_attributes = True