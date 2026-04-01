from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import psycopg2
from psycopg2.extras import execute_values

from encar_scraper.config import DATABASE_URL, db_params_from_url
from encar_scraper.listing_text import ParsedListing

logger = logging.getLogger(__name__)

DDL = """
CREATE TABLE IF NOT EXISTS encar_listings (
    car_id BIGINT PRIMARY KEY,
    brand TEXT NOT NULL DEFAULT '',
    model TEXT NOT NULL DEFAULT '',
    year TEXT,
    mileage INTEGER,
    price BIGINT,
    photo TEXT,
    detail_url TEXT NOT NULL DEFAULT '',
    title_raw TEXT,
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS encar_listings_updated_at_idx
    ON encar_listings (updated_at DESC);
"""

UPSERT = """
INSERT INTO encar_listings (
    car_id, brand, model, year, mileage, price,
    photo, detail_url, title_raw, scraped_at, updated_at
) VALUES %s
ON CONFLICT (car_id) DO UPDATE SET
    brand = EXCLUDED.brand,
    model = EXCLUDED.model,
    year = EXCLUDED.year,
    mileage = EXCLUDED.mileage,
    price = EXCLUDED.price,
    photo = EXCLUDED.photo,
    detail_url = EXCLUDED.detail_url,
    title_raw = EXCLUDED.title_raw,
    updated_at = EXCLUDED.updated_at;
"""


def connect():
    return psycopg2.connect(**db_params_from_url(DATABASE_URL))


def init_schema(cur) -> None:
    cur.execute(DDL)


def upsert_listings(rows: list[tuple[Any, ...]]) -> int:
    if not rows:
        return 0
    now = datetime.now(timezone.utc)

    by_car_id: dict[int, tuple] = {}
    for r in rows:
        car_id, parsed, photo_url, detail_url = r
        p: ParsedListing = parsed
        by_car_id[car_id] = (
            car_id,
            p.brand,
            p.model,
            p.year_label,
            p.mileage_km,
            p.price_krw,
            photo_url,
            detail_url,
            p.title_raw,
            now,
            now,
        )
    payload = list(by_car_id.values())
    if len(payload) < len(rows):
        logger.warning(
            "Deduplicated %s duplicate car_id rows before upsert",
            len(rows) - len(payload),
        )
    conn = connect()
    try:
        with conn.cursor() as cur:
            init_schema(cur)
            execute_values(cur, UPSERT, payload)
        conn.commit()
    finally:
        conn.close()
    logger.info("Upserted %s listings", len(payload))
    return len(payload)
