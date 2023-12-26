"""empty message

Revision ID: 70e96a3bae47
Revises: 
Create Date: 2023-12-26 08:29:37.507236

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '70e96a3bae47'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_time', sa.TIMESTAMP(), nullable=True))
        batch_op.add_column(sa.Column('end_time', sa.TIMESTAMP(), nullable=True))
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Text(),
               nullable=False)

    with op.batch_alter_table('cves', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)

    with op.batch_alter_table('exams', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
        batch_op.add_column(sa.Column('exam_duration', sa.Interval(), nullable=False))
        batch_op.drop_column('start_time')
        batch_op.drop_column('end_time')

    with op.batch_alter_table('exploits', schema=None) as batch_op:
        batch_op.alter_column('cve_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('exploit_path',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exploits', schema=None) as batch_op:
        batch_op.alter_column('exploit_path',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('cve_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('exams', schema=None) as batch_op:
        batch_op.add_column(sa.Column('end_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.drop_column('exam_duration')
        batch_op.drop_column('created_at')

    with op.batch_alter_table('cves', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)

    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=255),
               nullable=True)
        batch_op.drop_column('end_time')
        batch_op.drop_column('start_time')

    # ### end Alembic commands ###
