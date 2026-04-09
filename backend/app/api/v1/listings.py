from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...models import EncarListing
from ...schemas import ListingOut, ListingPage

router = APIRouter(prefix="/listings", tags=["listings"])


@router.get("", response_model=ListingPage)
def get_listings(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.scalar(select(func.count()).select_from(EncarListing)) or 0
    offset = (page - 1) * per_page
    rows = db.scalars(
        select(EncarListing).order_by(EncarListing.updated_at.desc()).offset(offset).limit(per_page)
    ).all()
    items = [
        ListingOut(
            car_id=r.car_id,
            brand=r.brand,
            model=r.model,
            year=r.year,
            mileage=r.mileage,
            price=r.price,
            photo=r.photo,
            detail_url=r.detail_url,
            updated_at=r.updated_at,
        )
        for r in rows
    ]
    return ListingPage(page=page, per_page=per_page, total=total, items=items)
