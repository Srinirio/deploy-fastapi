"""Expence model added

Revision ID: 2d8dc49a846c
Revises: 93ec04edde11
Create Date: 2024-09-23 10:00:41.359970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d8dc49a846c'
down_revision: Union[str, None] = '93ec04edde11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expense',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('approved_status', sa.Boolean(), nullable=True),
    sa.Column('approved_date', sa.DateTime(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('image', sa.String(length=200), nullable=True),
    sa.Column('emp_id', sa.String(length=20), nullable=False),
    sa.Column('approved_by', sa.String(length=20), nullable=True),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['approved_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['emp_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_expense_id'), 'expense', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_expense_id'), table_name='expense')
    op.drop_table('expense')
    # ### end Alembic commands ###