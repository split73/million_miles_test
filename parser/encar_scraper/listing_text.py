from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ParsedListing:
    brand: str
    model: str
    year_label: str | None
    mileage_km: int | None
    price_krw: int | None
    title_raw: str


def _strip_badges(s: str) -> str:
    s = s.strip()
    for pat in (
        r"^진단\+\+\s*",
        r"^진단\+\s*",
        r"^믿고\s*",
        r"^찜\s*",
    ):
        s = re.sub(pat, "", s)
    return s.strip()


def _extract_brand_model(before_year: str) -> tuple[str, str]:
    before_year = before_year.strip()
    m = re.match(r"^(\S+(?:\([^)]+\))?)\s+(.+)$", before_year)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return before_year, ""


def parse_listing_text(text: str) -> ParsedListing | None:
    text = text.replace("\n", " ")
    t = _strip_badges(text)
    if not t or "km" not in t.lower():
        return None

    km_m = re.search(r"([\d,]+)\s*km", t, re.I)
    mileage = int(km_m.group(1).replace(",", "")) if km_m else None

    price_m = re.search(r"([\d,]+)\s*만원", t)
    price_krw = int(price_m.group(1).replace(",", "")) * 10_000 if price_m else None

    parts = [p.strip() for p in t.split("·")]
    head = parts[0] if parts else t

    ym_head = re.search(r"(\d{2}/\d{2}식(?:\(\d{2}년형\))?)", head)
    year_label = ym_head.group(1) if ym_head else None

    if ym_head:
        before = head[: ym_head.start()].strip()
        brand, model = _extract_brand_model(before)
    else:
        brand, model = _extract_brand_model(head)

    return ParsedListing(
        brand=brand or "",
        model=model or "",
        year_label=year_label,
        mileage_km=mileage,
        price_krw=price_krw,
        title_raw=text.strip(),
    )
