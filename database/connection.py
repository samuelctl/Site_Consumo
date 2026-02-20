from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "postgresql+psycopg2://postgres:81848938spM!@localhost:5432/db_crud"

engine = create_engine( DATABASE_URL,echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()