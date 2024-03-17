"""add content column

Revision ID: e07bd69c84b7
Revises: d1afde917203
Create Date: 2024-03-17 17:47:54.462711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e07bd69c84b7'
down_revision: Union[str, None] = 'd1afde917203'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(150), nullable=False))
    pass


def downgrade() -> None:

    op.drop_column("posts", "content")
    pass
