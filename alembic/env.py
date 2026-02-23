from logging.config import fileConfig
import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from alembic import context

# Adiciona o diretório raiz ao sys.path para encontrar os modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Configuração do Alembic
config = context.config

# Configuração de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importa os modelos
from database.connection import Base
from models.usuario import Usuario
from models.consumo import Consumo

target_metadata = Base.metadata

# URL do banco de dados
DATABASE_URL = "postgresql+psycopg2://postgres:81848938spM!@localhost:5432/db_crud"

# Função para rodar migrations offline
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Função para rodar migrations online
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        echo=True  # opcional, mostra SQL no console
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Executa de acordo com o modo
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()