"""role: name field made unique

Revision ID: 053267007432
Revises: 156c06295ac2
Create Date: 2023-11-04 19:13:49.936639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "053267007432"
down_revision: Union[str, None] = "156c06295ac2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "role", ["name"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("role_name_key", "role", type_="unique")
    # ### end Alembic commands ###
