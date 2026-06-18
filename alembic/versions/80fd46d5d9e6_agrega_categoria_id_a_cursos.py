"""agrega categoria_id a cursos

Revision ID: 80fd46d5d9e6
Revises: 1dd7a4783b62
Create Date: 2026-06-18 15:22:29.931299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80fd46d5d9e6'
down_revision: Union[str, Sequence[str], None] = '1dd7a4783b62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('cursos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_cursos_categoria', 'categorias', ['categoria_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('cursos', schema=None) as batch_op:
        batch_op.drop_constraint('fk_cursos_categoria', type_='foreignkey')
        batch_op.drop_column('categoria_id')
