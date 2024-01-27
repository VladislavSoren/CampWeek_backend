"""deleted conection between Event and Speaker, Creator

Revision ID: 1ffe0260c9bd
Revises: 157aec38a17b
Create Date: 2023-11-03 22:39:31.410645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1ffe0260c9bd"
down_revision: Union[str, None] = "157aec38a17b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("event_speaker_id_fkey", "event", type_="foreignkey")
    op.drop_constraint("event_creator_id_fkey", "event", type_="foreignkey")
    op.drop_column("event", "creator_id")
    op.drop_column("event", "speaker_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("event", sa.Column("speaker_id", sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column("event", sa.Column("creator_id", sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key("event_creator_id_fkey", "event", "creator", ["creator_id"], ["id"])
    op.create_foreign_key("event_speaker_id_fkey", "event", "speaker", ["speaker_id"], ["id"])
    # ### end Alembic commands ###
