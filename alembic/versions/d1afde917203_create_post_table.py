"""create post table

Revision ID: d1afde917203
Revises: 
Create Date: 2024-03-16 23:17:06.607959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1afde917203'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True), sa.Column("title", sa.String(50), nullable=False))
    

    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
