"""empty message

Revision ID: 2fba210e9b13
Revises: 80cd7955b20c
Create Date: 2023-12-28 15:44:45.289537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fba210e9b13'
down_revision = '80cd7955b20c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('devices', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=10), nullable=True))

    with op.batch_alter_table('exploits', schema=None) as batch_op:
        batch_op.add_column(sa.Column('topic', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(length=10), nullable=False))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('status')

    with op.batch_alter_table('exploits', schema=None) as batch_op:
        batch_op.drop_column('status')
        batch_op.drop_column('topic')

    with op.batch_alter_table('devices', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
