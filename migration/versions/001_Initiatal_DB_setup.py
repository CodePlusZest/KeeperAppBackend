"""Initial database setup.

Revision ID: 001
Revises:
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_created_at", "users", ["created_at"], unique=False)

    op.create_table(
        "notes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=120), server_default=sa.text("''"), nullable=False),
        sa.Column("content", sa.Text(), server_default=sa.text("''"), nullable=False),
        sa.Column("status", sa.String(length=16), server_default=sa.text("'active'"), nullable=False),
        sa.Column("pinned", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status IN ('active', 'archived', 'trash')",
            name="ck_notes_status",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_notes_user_id", "notes", ["user_id"], unique=False)
    op.create_index("ix_notes_created_at", "notes", ["created_at"], unique=False)
    op.create_index("ix_notes_updated_at", "notes", ["updated_at"], unique=False)
    op.create_index(
        "ix_notes_status_updated_at",
        "notes",
        ["status", "updated_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_notes_status_updated_at", table_name="notes")
    op.drop_index("ix_notes_updated_at", table_name="notes")
    op.drop_index("ix_notes_created_at", table_name="notes")
    op.drop_index("ix_notes_user_id", table_name="notes")
    op.drop_table("notes")
    op.drop_index("ix_users_created_at", table_name="users")
    op.drop_table("users")