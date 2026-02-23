from database.connection import engine, Base, SessionLocal
from passlib.context import CryptContext
from schemas.Usuario import UsuarioCreate, UsuarioResponse
from schemas.Consumo import ConsumoCreate
from sqlalchemy.orm import Session
from main import app, get_db, Depends
from core.security import gerar_hash
from routers import regiao
import models


@app.post("/usuarios",response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db : Session = Depends(get_db)):
    senha_hash = gerar_hash.hash(usuario.senha)
    localidade= regiao.get_regiao_por_cidade(usuario.cidade)
    nome_regiao= "Não informada"
    if localidade and isinstance(localidade,dict):
        nome_regiao = localidade.get("regiao","Não encontrada")
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hash,
        cidade=usuario.cidade,
        regiao=nome_regiao
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario