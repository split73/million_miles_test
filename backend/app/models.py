from sqlalchemy import BigInteger, DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EncarListing(Base):
    __tablename__ = "encar_listings"

    car_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    brand: Mapped[str] = mapped_column(Text, default="", nullable=False)
    model: Mapped[str] = mapped_column(Text, default="", nullable=False)
    year: Mapped[str | None] = mapped_column(Text, nullable=True)
    mileage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    photo: Mapped[str | None] = mapped_column(Text, nullable=True)
    detail_url: Mapped[str] = mapped_column(Text, nullable=False, default="")
    title_raw: Mapped[str | None] = mapped_column(Text, nullable=True)
    scraped_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
