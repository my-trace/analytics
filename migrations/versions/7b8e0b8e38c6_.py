"""empty message

Revision ID: 7b8e0b8e38c6
Revises: e1d92b457bb0
Create Date: 2016-11-10 04:19:57.401581

"""

# revision identifiers, used by Alembic.
revision = '7b8e0b8e38c6'
down_revision = 'e1d92b457bb0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'points_account_id_fkey', 'points', type_='foreignkey')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(u'points_account_id_fkey', 'points', 'accounts', ['account_id'], ['id'])
    ### end Alembic commands ###