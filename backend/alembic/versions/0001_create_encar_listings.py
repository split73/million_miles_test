from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if inspect(bind).has_table("encar_listings"):
        return
    op.create_table(
        "encar_listings",
        sa.Column("car_id", sa.BigInteger(), nullable=False),
        sa.Column("brand", sa.Text(), nullable=False, server_default=""),
        sa.Column("model", sa.Text(), nullable=False, server_default=""),
        sa.Column("year", sa.Text(), nullable=True),
        sa.Column("mileage", sa.Integer(), nullable=True),
        sa.Column("price", sa.BigInteger(), nullable=True),
        sa.Column("photo", sa.Text(), nullable=True),
        sa.Column("detail_url", sa.Text(), nullable=False, server_default=""),
        sa.Column("title_raw", sa.Text(), nullable=True),
        sa.Column("scraped_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("car_id"),
    )
    op.create_index(
        "encar_listings_updated_at_idx",
        "encar_listings",
        ["updated_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("encar_listings_updated_at_idx", table_name="encar_listings")
    op.drop_table("encar_listings")
