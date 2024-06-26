"""Event: added new cols

Revision ID: 7e7a0723dacb
Revises: 70815b4c7cb7
Create Date: 2023-11-22 20:07:39.742146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7e7a0723dacb"
down_revision: Union[str, None] = "70815b4c7cb7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("event", sa.Column("link", sa.String(length=200), nullable=True))
    op.add_column("event", sa.Column("add_link", sa.String(length=200), nullable=True))
    op.add_column("event", sa.Column("time_start", sa.String(length=5), nullable=False))
    op.add_column("event", sa.Column("time_end", sa.String(length=5), nullable=False))
    op.add_column("event", sa.Column("is_reg_needed", sa.Boolean(), server_default=sa.text("true"), nullable=False))
    op.add_column("event", sa.Column("add_info", sa.Text(), nullable=True))
    op.add_column("event", sa.Column("notes", sa.Text(), nullable=True))
    op.alter_column(
        "event", "date_time", existing_type=postgresql.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True), existing_nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "event", "date_time", existing_type=sa.TIMESTAMP(timezone=True), type_=postgresql.TIMESTAMP(), existing_nullable=False
    )
    op.drop_column("event", "notes")
    op.drop_column("event", "add_info")
    op.drop_column("event", "is_reg_needed")
    op.drop_column("event", "time_end")
    op.drop_column("event", "time_start")
    op.drop_column("event", "add_link")
    op.drop_column("event", "link")
    # ### end Alembic commands ###
