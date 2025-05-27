from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import *
from .crud import *

router = APIRouter()


# ---- ROTAS USUÁRIOS ----

class UsuarioRoutes:
    def __init__(self, crud: CRUDUsuario):
        self.crud = crud

    def register_routes(self, router: APIRouter):
        @router.post("/usuarios/", response_model=UsuarioCreate)
        def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
            return self.crud.criar_usuario(db, usuario)

        @router.get("/usuarios/{usuario_id}", response_model=UsuarioCreate)
        def buscar_usuario(usuario_id: str, db: Session = Depends(get_db)):
            db_usuario = self.crud.buscar_usuario_por_id(db, usuario_id)
            if db_usuario is None:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            return db_usuario
        

# ---- ROTAS TIPO USUÁRIO ----

class TipoUsuarioRoutes:
    def __init__(self, crud: CRUDTipoUsuario):
        self.crud = crud

    def register_routes(self, router: APIRouter):
        @router.post("/tipos-usuario/", response_model=TipoUsuarioCreate)
        def criar_tipo(tipo: TipoUsuarioCreate, db: Session = Depends(get_db)):
            return self.crud.criar_tipo_usuario(db, tipo)

        @router.get("/tipos-usuario/", response_model=list[TipoUsuarioCreate])
        def listar_tipos(db: Session = Depends(get_db)):
            return self.crud.listar_tipos_usuario(db)
        

# ---- ROTAS TURMA ----

class TurmaRoutes:
    def __init__(self, crud: CRUDTurma):
        self.crud = crud

    def register_routes(self, router: APIRouter):
        @router.post("/turmas/", response_model=TurmaCreate)
        def criar_turma(turma: TurmaCreate, db: Session = Depends(get_db)):
            return self.crud.criar_turma(db, turma)

        @router.get("/turmas/", response_model=list[TurmaCreate])
        def listar_turmas(db: Session = Depends(get_db)):
            return self.crud.listar_turmas(db)
        

# ---- ROTAS CADASTRO ----

class CadastroRoutes:
    def __init__(self, crud: CRUDCadastro):
        self.crud = crud

    def register_routes(self, router: APIRouter):
        @router.post("/cadastro/", response_model=CadastroCreate)
        def criar_cadastro(cadastro: CadastroCreate, db: Session = Depends(get_db)):
            return self.crud.criar_cadastro(db, cadastro)

        @router.get("/cadastro/{usuario_id}", response_model=CadastroCreate)
        def buscar_cadastro(usuario_id: str, db: Session = Depends(get_db)):
            db_cadastro = self.crud.buscar_cadastro_por_id(db, usuario_id)
            if db_cadastro is None:
                raise HTTPException(status_code=404, detail="Cadastro não encontrado")
            return db_cadastro
        

# ---- ROTAS MATÉRIA ----

class MateriaRoutes:
    def __init__(self, crud: CRUDMateria):
        self.crud = crud

    def register_routes(self, router: APIRouter):
        @router.post("/materias/", response_model=MateriaCreate)
        def criar_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
            return self.crud.criar_materia(db, materia)

        @router.get("/materias/", response_model=list[MateriaCreate])
        def listar_materias(db: Session = Depends(get_db)):
            return self.crud.listar_materias(db)
        

# ---- ROTAS NÍVEL ----

class NivelRoutes:
    def __init__(self, crud: CRUDNivel):
        self.crud = crud
    def register_routes(self, router: APIRouter):
        @router.post("/niveis/", response_model=NivelCreate)
        def criar_nivel(nivel: NivelCreate, db: Session = Depends(get_db)):
            return self.crud.criar_nivel(db, nivel)

        @router.get("/niveis/", response_model=list[NivelCreate])
        def listar_niveis(db: Session = Depends(get_db)):
            return self.crud.listar_niveis(db)
        

# ---- ROTAS TIPO AJUDA ----

class TipoAjudaRoutes:
    def __init__(self, crud: CRUDTipoAjuda):
        self.crud = crud

    def register_routes(self, router: APIRouter):
        @router.post("/tipos_ajuda/", response_model=TipoAjudaCreate)
        def criar_tipo_ajuda(ajuda: TipoAjudaCreate, db: Session = Depends(get_db)):
            return self.crud.criar_tipo_ajuda(db, ajuda)

        @router.get("/tipos-ajuda/", response_model=list[TipoAjudaCreate])
        def listar_tipos_ajuda(db: Session = Depends(get_db)):
            return self.crud.listar_tipos_ajuda(db)
        

# ---- ROTAS QUESTÔES ----

class QuestaoRoutes:
    def __init__(self, crud: CRUDQuestao):
        self.crud = crud

    def register_routes(self, router: APIRouter):
        @router.post("/questoes/", response_model=QuestaoCreate)
        def criar_questao(questao: QuestaoCreate, db: Session = Depends(get_db)):
            return self.crud.criar_questao(db, questao)

        @router.get("/questoes/", response_model=list[QuestaoCreate])
        def buscar_questoes(materia_id: int, nivel_id: int, turma_id: int, db: Session = Depends(get_db)):
            return self.crud.buscar_questoes_por_materia_nivel_e_turma(db, materia_id, nivel_id, turma_id)
        

# ---- ROTAS SELECIONAR JOGO ----

class SelecionarJogoRoutes:
    def __init__(self, crud: CRUDSelecionarJogo):
        self.crud = crud

    def register_routes(self, router: APIRouter):
        @router.get("/selecionar-jogo/{usuario_id}", response_model=list[SelecionarJogoCreate])
        def listar_jogos(usuario_id: str, db: Session = Depends(get_db)):
            return self.crud.listar_jogos_usuario(db, usuario_id)
        

# ---- FUNÇÂO DE REGISTRO GERAL ----

def registar_todas_rotas():
    UsuarioRoutes(CRUDUsuario()).register_routes(router)
    TipoUsuarioRoutes(CRUDTipoUsuario()).register_routes(router)
    TurmaRoutes(CRUDTurma()).register_routes(router)
    CadastroRoutes(CRUDCadastro()).register_routes(router)
    MateriaRoutes(CRUDMateria()).register_routes(router)
    NivelRoutes(CRUDNivel()).register_routes(router)
    TipoAjudaRoutes(CRUDTipoAjuda()).register_routes(router)
    QuestaoRoutes(CRUDQuestao()).register_routes(router)
    SelecionarJogoRoutes(CRUDSelecionarJogo()).register_routes(router)