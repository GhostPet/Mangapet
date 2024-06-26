"""Added User Comic Perms

Revision ID: fa3e8f96794a
Revises: 96c513f5b8d5
Create Date: 2024-05-03 03:10:57.872550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa3e8f96794a'
down_revision = '96c513f5b8d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comic_users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('can_add_chapters', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('can_edit_chapters', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('can_delete_chapters', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comic_users', schema=None) as batch_op:
        batch_op.drop_column('can_delete_chapters')
        batch_op.drop_column('can_edit_chapters')
        batch_op.drop_column('can_add_chapters')

    # ### end Alembic commands ###
