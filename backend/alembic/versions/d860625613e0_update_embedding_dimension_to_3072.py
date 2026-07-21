"""update embedding dimension to 3072

Revision ID: d860625613e0
Revises: 0ca956621c61
Create Date: 2026-07-21 14:51:37.803129

"""

from typing import Sequence, Union

from alembic import op
from pgvector.sqlalchemy import VECTOR

# revision identifiers, used by Alembic.
revision: str = "d860625613e0"
down_revision: Union[str, Sequence[str], None] = "0ca956621c61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        "document_chunks",
        "embedding",
        existing_type=VECTOR(dim=768),
        type_=VECTOR(dim=3072),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "document_chunks",
        "embedding",
        existing_type=VECTOR(dim=3072),
        type_=VECTOR(dim=768),
        existing_nullable=False,
    )