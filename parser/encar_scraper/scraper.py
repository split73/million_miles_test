from __future__ import annotations

import json
import logging
import re
import time
from urllib.parse import quote

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from encar_scraper.config import (
    ENCAR_LIST_BASE,
    ENCAR_LIST_WAIT_SEC,
    ENCAR_MAX_PAGES,
    ENCAR_PAGE_LIMIT,
)
from encar_scraper.db import upsert_listings
from encar_scraper.listing_text import ParsedListing, parse_listing_text

logger = logging.getLogger(__name__)

LISTING_SELECTOR = "a[href*='dc_cardetailview.do'][href*='carid=']"


def _build_list_url(page: int) -> str:
    state = {
        "action": "(And.Hidden.N._.CarType.Y.)",
        "toggle": {},
        "layer": "",
        "sort": "ModifiedDate",
        "page": page,
        "limit": ENCAR_PAGE_LIMIT,
        "searchKey": "",
        "loginCheck": False,
    }
    frag = quote(json.dumps(state, separators=(",", ":")), safe="")
    return f"{ENCAR_LIST_BASE}#!{frag}"


def _car_id_from_href(href: str) -> str | None:
    m = re.search(r"carid=(\d+)", href)
    return m.group(1) if m else None


def _photo_near_anchor(anchor, car_id: str) -> str:
    el = anchor
    for _ in range(18):
        try:
            el = el.find_element(By.XPATH, "..")
        except Exception:
            break
        for img in el.find_elements(By.CSS_SELECTOR, "img[src*='carpicture']"):
            src = (img.get_attribute("src") or "").strip()
            if car_id in src:
                return src
    return ""


def _dedupe_best_anchors(driver) -> list:
    anchors = driver.find_elements(By.CSS_SELECTOR, LISTING_SELECTOR)
    best: dict[str, tuple[int, object]] = {}
    for a in anchors:
        href = a.get_attribute("href") or ""
        cid = _car_id_from_href(href)
        if not cid:
            continue
        txt = (a.text or "").strip()
        score = len(txt)
        if cid not in best or score > best[cid][0]:
            best[cid] = (score, a)
    return [best[k][1] for k in sorted(best.keys(), key=int)]


def scrape_page(driver, page: int) -> list[tuple[int, ParsedListing, str, str]]:
    url = _build_list_url(page)
    logger.info("Loading page %s", page)
    driver.get(url)
    try:
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except TimeoutException:
        logger.warning("Body timeout on page %s", page)
        return []
    time.sleep(ENCAR_LIST_WAIT_SEC)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, LISTING_SELECTOR))
    )

    out: list[tuple[int, ParsedListing, str, str]] = []
    for a in _dedupe_best_anchors(driver):
        href = (a.get_attribute("href") or "").strip()
        cid_s = _car_id_from_href(href)
        if not cid_s:
            continue
        text = (a.text or "").strip()
        parsed = parse_listing_text(text)
        if not parsed:
            continue
        photo = _photo_near_anchor(a, cid_s)
        out.append((int(cid_s), parsed, photo, href))
    logger.info("Parsed %s listings on page %s", len(out), page)
    return out


def make_driver(headless: bool = True) -> webdriver.Chrome:
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--lang=ko-KR")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


def run_scrape(headless: bool = True) -> int:
    total_rows: list[tuple[int, ParsedListing, str, str]] = []
    driver = make_driver(headless=headless)
    try:
        for p in range(1, ENCAR_MAX_PAGES + 1):
            rows = scrape_page(driver, p)
            total_rows.extend(rows)
            if not rows:
                break
    finally:
        driver.quit()
    return upsert_listings(total_rows)
