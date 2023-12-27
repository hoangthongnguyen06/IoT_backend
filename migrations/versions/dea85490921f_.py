"""empty message

Revision ID: dea85490921f
Revises: 48bb49c06bac
Create Date: 2023-12-27 07:54:16.288633

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dea85490921f'
down_revision = '48bb49c06bac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exams', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.drop_constraint('exams_course_id_fkey', type_='foreignkey')
        batch_op.drop_column('course_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exams', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('exams_course_id_fkey', 'courses', ['course_id'], ['id'])
        batch_op.alter_column('created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    # ### end Alembic commands ###
