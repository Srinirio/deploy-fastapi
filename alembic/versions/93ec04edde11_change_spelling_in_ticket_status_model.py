"""change spelling in ticket status model

Revision ID: 93ec04edde11
Revises: 6f43b721f23c
Create Date: 2024-09-20 18:02:23.152383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '93ec04edde11'
down_revision: Union[str, None] = '6f43b721f23c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticket_status', sa.Column('completed_date', sa.DateTime(), nullable=True))
    op.drop_column('ticket_status', 'compiled_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticket_status', sa.Column('compiled_date', mysql.DATETIME(), nullable=True))
    op.drop_column('ticket_status', 'completed_date')
    # ### end Alembic commands ###