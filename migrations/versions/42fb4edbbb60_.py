"""empty message

Revision ID: 42fb4edbbb60
Revises: fbee37e57ff4
Create Date: 2023-12-26 10:20:07.973358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42fb4edbbb60'
down_revision = 'fbee37e57ff4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exams', schema=None) as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exams', schema=None) as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
