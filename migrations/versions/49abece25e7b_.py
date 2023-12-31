"""empty message

Revision ID: 49abece25e7b
Revises: 7f906d88100c
Create Date: 2023-12-26 10:50:38.798199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49abece25e7b'
down_revision = '7f906d88100c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exams', schema=None) as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exams', schema=None) as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
