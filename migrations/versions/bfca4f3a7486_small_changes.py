"""Small Changes

Revision ID: bfca4f3a7486
Revises: 3ef6d08cfc9c
Create Date: 2024-04-29 19:01:43.898111

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bfca4f3a7486'
down_revision = '3ef6d08cfc9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_permissions', schema=None) as batch_op:
        batch_op.drop_column('is_banned')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_banned', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_banned')

    with op.batch_alter_table('user_permissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_banned', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
