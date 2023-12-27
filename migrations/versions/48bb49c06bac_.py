"""empty message

Revision ID: 48bb49c06bac
Revises: 28dbeea53e1c
Create Date: 2023-12-27 07:52:46.395056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48bb49c06bac'
down_revision = '28dbeea53e1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exams', schema=None) as batch_op:
        batch_op.drop_column('score')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exams', schema=None) as batch_op:
        batch_op.add_column(sa.Column('score', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))

    # ### end Alembic commands ###