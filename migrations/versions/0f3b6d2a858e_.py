"""empty message

Revision ID: 0f3b6d2a858e
Revises: bd837c2985e8
Create Date: 2016-11-10 04:40:43.831901

"""

# revision identifiers, used by Alembic.
revision = '0f3b6d2a858e'
down_revision = 'bd837c2985e8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('facebook_id', sa.BigInteger(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'facebook_id')
    ### end Alembic commands ###
