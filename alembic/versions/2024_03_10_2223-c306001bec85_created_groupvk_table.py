"""created GroupVK table

Revision ID: c306001bec85
Revises: ae23866f2b2b
Create Date: 2024-03-10 22:23:50.943606

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c306001bec85"
down_revision: Union[str, None] = "ae23866f2b2b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "groupvk",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("token", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("token"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("groupvk")
    # ### end Alembic commands ###