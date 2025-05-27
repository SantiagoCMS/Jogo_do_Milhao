from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import (
    Usuario, TipoUsuario, Turma, Cadastro, Materia,
    Nivel, TipoAjuda, Questao, SelecionarJogo
)
from .schemas import (
    UsuarioCreate, TipoUsuarioCreate, TurmaCreate, CadastroCreate,
    MateriaCreate, NivelCreate, TipoAjudaCreate, QuestaoCreate,
    SelecionarJogoCreate, 
)
from typing import List, Optional
from datetime import datetime


# ---- CRUD USUÁRIO ----

class CRUDUsuario:
    def criar_usuario(self, db: Session, usuario: UsuarioCreate):
        db_usuario = Usuario(**usuario.dict())
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    def buscar_usuario_por_id(self, db: Session, id_usuario: str):
        return db.query(Usuario).filter(Usuario.idUsuario == id_usuario).first()


# ---- CRUD TIPO USUÁRIO ----

class CRUDTipoUsuario:
    def criar_tipo_usuario(self, db: Session, tipo_usuario: TipoUsuarioCreate):
        db_tipo_usuario = TipoUsuario(**tipo_usuario.dict())
        db.add(db_tipo_usuario)
        db.commit()
        db.refresh(db_tipo_usuario)
        return db_tipo_usuario
    
    def listar_tipos_usuario(self, db: Session, id_tipo_usuario: int):
        return db.query(TipoUsuario).all()
    

# ---- CRUD TURMA ----

class CRUDTurma:
    def criar_turma(self, db: Session, turma: TurmaCreate):
        db_turma = Turma(**turma.dict())
        db.add(db_turma)
        db.commit()
        db.refresh(db_turma)
        return db_turma
    
    def listar_turmas(self, db: Session):
        return db.query(Turma).all()
    
    def buscar_turma_por_id(self, db: Session, id_turma: int):
        return db.query(Turma).filter(Turma.codigoTurma == id_turma).first()
    

# ---- CRUD CADASTRO ----

class CRUDCadastro:
    def criar_cadastro(self, db: Session, cadastro: CadastroCreate):
        db_cadastro = Cadastro(**cadastro.dict())
        db.add(db_cadastro)
        db.commit()
        db.refresh(db_cadastro)
        return db_cadastro
    
    def listar_cadastros(self, db: Session):
        return db.query(Cadastro).all()
    
    def buscar_cadastro_por_id(self, db: Session, id_usuario: str):
        return db.query(Cadastro).filter(Cadastro.Usuario_idUsuario == id_usuario).first()
    

# ---- CRUD MATÉRIA ----

class CRUDMateria:
    def criar_materia(self, db: Session, materia: MateriaCreate):
        db_materia = Materia(**materia.dict())
        db.add(db_materia)
        db.commit()
        db.refresh(db_materia)
        return db_materia
    
    def listar_materias(self, db: Session):
        return db.query(Materia).all()
    
    def buscar_materia_por_id(self, db: Session, id_materia: int):
        return db.query(Materia).filter(Materia.idMateria == id_materia).first()
    

# ---- CRUD NÍVEL ----

class CRUDNivel:
    def criar_nivel(self, db: Session, nivel: NivelCreate):
        db_nivel = Nivel(**nivel.dict())
        db.add(db_nivel)
        db.commit()
        db.refresh(db_nivel)
        return db_nivel
    
    def listar_niveis(self, db: Session):
        return db.query(Nivel).all()
    
    def buscar_nivel_por_id(self, db: Session, id_nivel: int):
        return db.query(Nivel).filter(Nivel.idNivel == id_nivel).first()
    

# ---- CRUD TIPO AJUDA ----

class CRUDTipoAjuda:
    def criar_tipo_ajuda(self, db: Session, tipo_ajuda: TipoAjudaCreate):
        db_tipo_ajuda = TipoAjuda(**tipo_ajuda.dict())
        db.add(db_tipo_ajuda)
        db.commit()
        db.refresh(db_tipo_ajuda)
        return db_tipo_ajuda
    
    def listar_tipos_ajuda(self, db: Session):
        return db.query(TipoAjuda).all()
    
    def buscar_tipo_ajuda_por_id(self, db: Session, id_tipo_ajuda: int):
        return db.query(TipoAjuda).filter(TipoAjuda.codAjuda == id_tipo_ajuda).first()
    

# ---- CRUD QUESTÕES ----

class CRUDQuestao:
    def criar_questao(self, db: Session, questao: QuestaoCreate):
        db_questao = Questao(**questao.dict())
        db.add(db_questao)
        db.commit()
        db.refresh(db_questao)
        return db_questao
    
    def buscar_questoes_por_materia_nivel_e_turma(self, db: Session, materia_id: int, nivel_id: int, turma_id: int):
        return db.query(Questao)\
            .join(SelecionarJogo)\
            .filter(
                SelecionarJogo.Materia_idMateria == materia_id,
                SelecionarJogo.Nivel_idNivel == nivel_id,
                SelecionarJogo.Turma_codigoTurma == turma_id
            ).all()
    

# ---- CRUD SELECIONAR JOGO ----

class CRUDSelecionarJogo:
    def registrar_selecao(self, db: Session, selecionar_jogo: SelecionarJogoCreate):
        db_selecionar_jogo = SelecionarJogo(**selecionar_jogo.dict())
        db.add(db_selecionar_jogo)
        db.commit()
        db.refresh(db_selecionar_jogo)
        return db_selecionar_jogo
    
    def listar_jogos_usuario(self, db: Session, id_usuario: str):
        return db.query(SelecionarJogo).filter(
            SelecionarJogo.Cadastro_Usuario_idUsuario == id_usuario
        ).all()
    
    def buscar_selecionar_jogo_por_id(self, db: Session, id_selecionar_jogo: int):
        return db.query(SelecionarJogo).filter(SelecionarJogo.idSelecionarJogo == id_selecionar_jogo).first()