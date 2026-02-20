from database.connection import engine, Base, SessionLocal
from passlib.context import CryptContext
from schemas.Usuario import UsuarioCreate, UsuarioResponse
from schemas.Consumo import ConsumoCreate
from sqlalchemy.orm import Session
from main import app, get_db, Depends
from core.security import gerar_hash
import models


@app.post("/usuarios",response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db : Session = Depends(get_db)):
    senha_hash = gerar_hash.hash(usuario.senha)

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hash
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario