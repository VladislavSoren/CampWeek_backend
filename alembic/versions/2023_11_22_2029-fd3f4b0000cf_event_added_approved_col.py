"""Event: added approved col

Revision ID: fd3f4b0000cf
Revises: 7e7a0723dacb
Create Date: 2023-11-22 20:29:03.586928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fd3f4b0000cf"
down_revision: Union[str, None] = "7e7a0723dacb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("event", sa.Column("approved", sa.Boolean(), server_default=sa.text("false"), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("event", "approved")
    # ### end Alembic commands ###
