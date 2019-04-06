"""empty message

Revision ID: 2a60ad5145f5
Revises: 
Create Date: 2019-04-04 12:15:30.878017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a60ad5145f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'players', ['player_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'players', type_='unique')
    # ### end Alembic commands ###
