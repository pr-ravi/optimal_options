"""base schema

Revision ID: 16527ce62701
Revises: 7db6e800af71
Create Date: 2022-01-27 15:04:24.942998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16527ce62701'
down_revision = '7db6e800af71'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'history',
        sa.Column('instrument', sa.String(15), primary_key= True),
        sa.Column('exchange', sa.String(15), primary_key=True),
        sa.Column('date', sa.Date, primary_key=True),
        sa.Column('open', sa.Numeric(10)),
        sa.Column('close', sa.Numeric(10)),
        sa.Column('high', sa.Numeric(10)),
        sa.Column('low', sa.Numeric(10)),
        sa.Column('volume', sa.Integer)
    )

    op.create_table(
        'instrument_list',
        sa.Column('id', sa.Integer, autoincrement=True),
        sa.Column('type', sa.String(10)),
        sa.Column('values', sa.Text)
    )


def downgrade():
    op.drop_table('history')
    op.drop_table('instrument_list')
