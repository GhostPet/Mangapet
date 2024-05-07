"""Added comic cover

Revision ID: 4801eed725e7
Revises: 1b48dcfef6ae
Create Date: 2024-04-30 20:04:24.377069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4801eed725e7'
down_revision = '1b48dcfef6ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comics', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cover_img', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comics', schema=None) as batch_op:
        batch_op.drop_column('cover_img')

    # ### end Alembic commands ###