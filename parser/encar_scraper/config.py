import os
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return int(raw)


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return raw.lower() in ("1", "true", "yes", "on")


DATABASE_URL = os.environ.get("DATABASE_URL", "")
ENCAR_MAX_PAGES = _env_int("ENCAR_MAX_PAGES", 5)
ENCAR_PAGE_LIMIT = _env_int("ENCAR_PAGE_LIMIT", 20)
ENCAR_LIST_WAIT_SEC = _env_int("ENCAR_LIST_WAIT_SEC", 8)
SCRAPE_ONCE = _env_bool("SCRAPE_ONCE", False)

SCHEDULE_HOUR = _env_int("SCHEDULE_HOUR", 3)
SCHEDULE_MINUTE = _env_int("SCHEDULE_MINUTE", 0)
_SCHED_TZ = os.environ.get("SCHEDULE_TIMEZONE", "UTC")
try:
    from zoneinfo import ZoneInfo

    SCHEDULE_TIMEZONE = ZoneInfo(_SCHED_TZ)
except Exception:
    SCHEDULE_TIMEZONE = ZoneInfo("UTC")

ENCAR_LIST_BASE = (
    "https://www.encar.com/dc/dc_carsearchlist.do?carType=kor"
)


def db_params_from_url(url: str) -> dict:
    if not url:
        raise ValueError("DATABASE_URL is not set")
    p = urlparse(url)
    if p.scheme not in ("postgresql", "postgres"):
        raise ValueError("DATABASE_URL must be a postgres URL")
    db = (p.path or "").lstrip("/")
    return {
        "host": p.hostname or "localhost",
        "port": p.port or 5432,
        "user": p.username,
        "password": p.password,
        "dbname": db,
    }
