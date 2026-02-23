"""adiciona colunas cidade e regiao

Revision ID: f7d6782c4d18
Revises: 
Create Date: 2026-02-21 11:59:33.269038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7d6782c4d18'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Adiciona as colunas como nullable=True primeiro
    op.add_column('usuarios', sa.Column('cidade', sa.String(length=100), nullable=True))
    op.add_column('usuarios', sa.Column('regiao', sa.String(length=50), nullable=True))

    # Atualiza valores nulos existentes para algum valor default
    op.execute("UPDATE usuarios SET cidade = 'Desconhecido' WHERE cidade IS NULL")
    op.execute("UPDATE usuarios SET regiao = 'Desconhecida' WHERE regiao IS NULL")

    # Altera as colunas para NOT NULL
    op.alter_column('usuarios', 'cidade', nullable=False)
    op.alter_column('usuarios', 'regiao', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('usuarios', 'regiao')
    op.drop_column('usuarios', 'cidade')
