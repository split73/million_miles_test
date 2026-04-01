"""rename russian columns to english

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-01
"""

from alembic import op
from sqlalchemy import inspect


revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def _has_column(inspector, table_name: str, column_name: str) -> bool:
    return any(c["name"] == column_name for c in inspector.get_columns(table_name))


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("encar_listings"):
        return

    rename_pairs = [
        ("марка", "brand"),
        ("модель", "model"),
        ("год", "year"),
        ("пробег", "mileage"),
        ("цена", "price"),
        ("фото", "photo"),
    ]

    for old_name, new_name in rename_pairs:
        if _has_column(inspector, "encar_listings", old_name) and not _has_column(
            inspector, "encar_listings", new_name
        ):
            op.execute(f'ALTER TABLE encar_listings RENAME COLUMN "{old_name}" TO {new_name}')
            inspector = inspect(bind)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("encar_listings"):
        return

    rename_pairs = [
        ("brand", "марка"),
        ("model", "модель"),
        ("year", "год"),
        ("mileage", "пробег"),
        ("price", "цена"),
        ("photo", "фото"),
    ]

    for old_name, new_name in rename_pairs:
        if _has_column(inspector, "encar_listings", old_name) and not _has_column(
            inspector, "encar_listings", new_name
        ):
            op.execute(f'ALTER TABLE encar_listings RENAME COLUMN {old_name} TO "{new_name}"')
            inspector = inspect(bind)
