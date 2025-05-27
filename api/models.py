from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, CHAR
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


# Armazena tipos de usuários
class TipoUsuario(Base):
    __tablename__ = 'tipo_usuario'

    id = Column('idTipo_Usuario', Integer, primary_key=True) # Chave primária
    nome = Column('tipoUsuario', String(15), nullable=False) # Nome do tipo de usuário, obrigatório
    usuarios = relationship("Usuario", back_populates="tipo") # Relacionamento com a tabela Usuario


# Representa turmas (Ensino Fundamental ou Ensino Médio)
class Turma(Base):
    __tablename__ = 'turma'

    id = Column('codigoTurma', Integer, primary_key=True) # Chave primária
    nome = Column('nomeTurma', String(30), nullable=False) # Nome da turma, obrigatório (E.F. ou E.M.)
    usuarios = relationship("Usuario", back_populates="turma") # Relacionamento com a tabela Usuario


#Armazena dados dos usuários
class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column('idUsuario', CHAR(15), primary_key=True) # Chave primária
    nome = Column('nomeUsuario', String(60), nullable=False) # Nome do usuário, obrigatório
    senha = Column('senhaUsuario', String(45), nullable=False) # Armazenar hash da senha
    tipo_id = Column('Tipo_Usuario_idTipo_Usuario', Integer, ForeignKey('tipo_usuario.idTipo_Usuario')) # Chave estrangeira referenciando a tabela TipoUsuario
    turma_id = Column('Turma_codigoTurma', Integer, ForeignKey('turma.codigoTurma')) # Chave estrangeira referenciando a tabela Turma

    tipo = relationship("TipoUsuario", back_populates="usuarios") # Relacionamento com a tabela TipoUsuario
    turma = relationship("Turma", back_populates="usuarios") # Relacionamento com a tabela Turma
    pontuacoes = relationship("Pontuacao", back_populates="usuario") # Relacionamento com a tabela Pontuacao
    jogos_realizados = relationship("JogoRealizado", back_populates="usuario") # Relacionamento com a tabela JogoRealizado


# Define níveis de dificuldade (Fácil, Médio, Difícil)
class Nivel(Base):
    __tablename__ = 'nivel'

    id = Column('idNivel', Integer, primary_key=True) # Chave primária
    descricao = Column('descricaoNivel', String(20), nullable=False) # Descrição do nível, obrigatório


# Armazena matérias (Matemática, História...)
class Materia(Base):
    __tablename__ = 'materia'

    id = Column('idMateria', Integer, primary_key=True) # Chave primária
    nome = Column('nomeMateria', String(25), nullable=False) # Nome da matéria, obrigatório


# Tipos de ajuda)
class TipoAjuda(Base):
    __tablename__ = 'tipoajuda'

    id = Column('codAjuda', Integer, primary_key=True) # Chave primária
    nome = Column('nomeAjuda', String(45), nullable=False) # Dica, Pular Questão...


# Armazena enunciados e alternativas de questões
class Questao(Base):
    __tablename__ = 'questao_alternativa'

    id = Column('idQuestaoAlternativa', Integer, primary_key=True) # Chave primária
    enunciado = Column('Enunciado', Text, nullable=False) # Enunciado da questão, obrigatório
    resposta_correta = Column('respostaCorreta', String(45), nullable=False) # Resposta certa
    alternativa_a = Column('AlternativaA', String(45)) # Alternativa A
    alternativa_b = Column('AlternativaB', String(45)) # B
    alternativa_c = Column('AlternativaC', String(45)) # C
    alternativa_d = Column('AlternativaD', String(45)) # D
    

# Registra os jogos realizados pelos usuários
class SelecionarJogo(Base):
    __tablename__ = 'jogo_realizado'

    id = Column(Integer, primary_key=True) # Chave primária
    usuario_id = Column(CHAR(15), ForeignKey('usuario.idUsuario')) # Chave estrangeira referenciando a tabela Usuario
    questao_id = Column(Integer, ForeignKey('questao_alternativa.idQuestaoAlternativa')) # Chave estrangeira referenciando a tabela Questao
    ajuda_id = Column(Integer, ForeignKey('tipoajuda.codAjuda')) # Chave estrangeira referenciando a tabela TipoAjuda
    acertou = Column(Boolean, nullable=False) # Se o usuário acertou ou não
    data = Column(DateTime, default=datetime.utcnow) # Data e hora do jogo, padrão UTC

    usuario = relationship("Usuario", back_populates="jogos_realizados") # Relacionamento com a tabela Usuario


# Armazena pontuações dos usuários
class Pontuacao(Base):
    __tablename__ = 'pontuacao'

    id = Column(Integer, primary_key=True) # Chave primária
    usuario_id = Column(CHAR(15), ForeignKey('usuario.idUsuario')) # Chave estrangeira referenciando a tabela Usuario
    pontos = Column(Integer, nullable=False) # Pontos ganhos
    data = Column(DateTime, default=datetime.utcnow) # Data e hora da pontuação, padrão UTC
    materia_id = Column(Integer, ForeignKey('materia.idMateria')) # Chave estrangeira referenciando a tabela Materia
    nivel_id = Column(Integer, ForeignKey('nivel.idNivel')) # Chave estrangeira referenciando a tabela Nivel

    usuario = relationship("Usuario", back_populates="pontuacoes") # Relacionamento com a tabela Usuario

# Cadastro dos Usuários
class Cadastro(Base):
    __tablename__ = 'cadastro_usuario'

    id = Column(Integer, primary_key=True) # Chave primária
    usuario_id = Column(CHAR(15), ForeignKey('usuario.idUsuario')) # Chave estrangeira referenciando a tabela Usuario
    data_cadastro = Column(DateTime, default=datetime.utcnow) # Data e hora do cadastro, padrão UTC

    usuario = relationship("Usuario", back_populates="cadastro") # Relacionamento com a tabela Usuario