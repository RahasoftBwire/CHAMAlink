"""Add default_currency_id to Chama model

Revision ID: 45ca65d842ad
Revises: bf927dfa1ec5
Create Date: 2025-07-13 02:57:50.156748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45ca65d842ad'
down_revision = 'bf927dfa1ec5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currencies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=3), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('symbol', sa.String(length=5), nullable=False),
    sa.Column('exchange_rate_to_usd', sa.Float(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    with op.batch_alter_table('chamas', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'currencies', ['default_currency_id'], ['id'])

    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('currency_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'currencies', ['currency_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('currency_id')

    with op.batch_alter_table('chamas', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    op.drop_table('currencies')
    # ### end Alembic commands ###
