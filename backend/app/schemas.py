from datetime import datetime

from pydantic import BaseModel


class ListingOut(BaseModel):
    car_id: int
    brand: str
    model: str
    year: str | None
    mileage: int | None
    price: int | None
    photo: str | None
    detail_url: str
    updated_at: datetime | None


class ListingPage(BaseModel):
    page: int
    per_page: int
    total: int
    items: list[ListingOut]
