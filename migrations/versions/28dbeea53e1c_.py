"""empty message

Revision ID: 28dbeea53e1c
Revises: 5d07594ed355
Create Date: 2023-12-27 07:33:25.391207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28dbeea53e1c'
down_revision = '5d07594ed355'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_exam_association', schema=None) as batch_op:
        batch_op.add_column(sa.Column('score', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_exam_association', schema=None) as batch_op:
        batch_op.drop_column('score')

    # ### end Alembic commands ###
