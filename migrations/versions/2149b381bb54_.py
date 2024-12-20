"""empty message

Revision ID: 2149b381bb54
Revises: b0ed0ab686e1
Create Date: 2024-11-21 15:46:16.618586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2149b381bb54'
down_revision = 'b0ed0ab686e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_username'), type_='unique')

    # ### end Alembic commands ###
