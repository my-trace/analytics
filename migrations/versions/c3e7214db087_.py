"""empty message

Revision ID: c3e7214db087
Revises: 0f3b6d2a858e
Create Date: 2016-11-10 04:54:14.691358

"""

# revision identifiers, used by Alembic.
revision = 'c3e7214db087'
down_revision = '0f3b6d2a858e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('facebook_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('points',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('lng', sa.Float(), nullable=False),
    sa.Column('alt', sa.Float(), nullable=True),
    sa.Column('floor_level', sa.Integer(), nullable=True),
    sa.Column('vertical_accuracy', sa.Float(), nullable=True),
    sa.Column('horizontal_accuracy', sa.Float(), nullable=True),
    sa.Column('account_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('points')
    op.drop_table('accounts')
    ### end Alembic commands ###
