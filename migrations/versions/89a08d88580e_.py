"""empty message

Revision ID: 89a08d88580e
Revises: 49abece25e7b
Create Date: 2023-12-26 11:49:49.504700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89a08d88580e'
down_revision = '49abece25e7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course_exam_association',
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('course_exam_association')
    # ### end Alembic commands ###
