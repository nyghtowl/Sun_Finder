"""Add zoomlevel to locations.

Revision ID: 3c49d7378623
Revises: 4bb493e1febb
Create Date: 2013-09-14 00:14:54.565243

"""

# revision identifiers, used by Alembic.
revision = '3c49d7378623'
down_revision = '4bb493e1febb'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

def upgrade():
    op.add_column('location', sa.Column('zoomlevel', sa.Integer))

    location = table('location',
        column('zoomlevel', sa.Integer)
    )
    op.execute(
        location.update().values({'zoomlevel':13})
    )    

def downgrade():
    op.drop_column('location', 'zoomlevel')
