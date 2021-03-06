"""empty message

Revision ID: f68cc3af0c0d
Revises: 11191feb3c87
Create Date: 2016-09-02 14:44:57.490547

"""

# revision identifiers, used by Alembic.
revision = 'f68cc3af0c0d'
down_revision = '11191feb3c87'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'points_account_id_fkey', 'points', type_='foreignkey')
    op.drop_column('points', 'account_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('points', sa.Column('account_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'points_account_id_fkey', 'points', 'accounts', ['account_id'], ['id'])
    ### end Alembic commands ###
