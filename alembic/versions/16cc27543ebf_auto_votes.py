"""auto-votes

Revision ID: 16cc27543ebf
Revises: 5277d89314b5
Create Date: 2024-03-17 19:06:59.350851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '16cc27543ebf'
down_revision: Union[str, None] = '5277d89314b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.add_column('posts', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.alter_column('posts', 'published',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True,
               existing_server_default=sa.text("'1'"))
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=60),
               type_=sa.String(length=50),
               existing_nullable=False)
    op.alter_column('users', 'created_at',
               existing_type=mysql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.alter_column('users', 'created_at',
               existing_type=mysql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('users', 'email',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=60),
               existing_nullable=False)
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.alter_column('posts', 'published',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False,
               existing_server_default=sa.text("'1'"))
    op.drop_column('posts', 'updated_at')
    op.drop_table('votes')
    # ### end Alembic commands ###