from sqlalchemy import Column, Integer, String
from database.connection import Base, SessionLocal
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    consumos = relationship("Consumo", back_populates="usuario")
db = SessionLocal()
db.close()