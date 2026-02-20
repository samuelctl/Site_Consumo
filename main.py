from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database.connection import engine, Base, SessionLocal
from passlib.context import CryptContext
from schemas.Usuario import UsuarioCreate, UsuarioResponse
from core.security import gerar_hash, verificar_senha
from schemas.Consumo import ConsumoCreate
from schemas.login import LoginRequest
from fastapi import HTTPException
import models.consumo
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers = ["*"]
)

@app.post("/usuarios",response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db : Session = Depends(get_db)):
    senha_hash = gerar_hash(usuario.senha)

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hash
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    print("Seja bem vindo: ", novo_usuario.nome, "ID: ", novo_usuario.id) 
    return novo_usuario

@app.post("/login", response_model=UsuarioResponse)
def login(dados: LoginRequest,db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == dados.email 
    ).first()

    if not usuario or not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(status_code=400, detail="Email ou senha inválidos!!")
    return usuario


@app.post("/consumos")
def criar_consumo(dados: ConsumoCreate, db: Session = Depends(get_db)):
    novo_cons = models.consumo.Consumo(
        tipo=dados.tipo,
        gasto=dados.gasto,
        usuario_id=dados.usuario_id,
        data=dados.data
    )
    db.add(novo_cons)
    db.commit()
    db.refresh(novo_cons)
    return {"status": "Consumo registrado!"}

@app.get("/consumos/usuario/{u_id}")
def listar_consumos(u_id: int, db: Session = Depends(get_db)):
    # Busca todos os consumos onde o usuario_id é igual ao ID passado na URL
    lista = db.query(models.consumo.Consumo).filter(
        models.consumo.Consumo.usuario_id == u_id
    ).all()
    return lista

@app.delete("/consumos/{consumo_id}")
def deletar_consumo(consumo_id: int, db: Session = Depends(get_db)):
    db_consumo = db.query(models.consumo.Consumo).filter(models.consumo.Consumo.id == consumo_id).first()
    if not db_consumo:
        raise HTTPException(status_code=404, detail="Consumo não encontrado")
    db.delete(db_consumo)
    db.commit()
    return {"detail": "Deletado com sucesso"}