from __future__ import annotations

import logging
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from encar_scraper.config import (
    SCRAPE_ONCE,
    SCHEDULE_HOUR,
    SCHEDULE_MINUTE,
    SCHEDULE_TIMEZONE,
)
from encar_scraper.scraper import run_scrape

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("encar.main")


def job() -> None:
    try:
        n = run_scrape(headless=True)
        log.info("Scrape finished, saved rows: %s", n)
    except Exception:
        log.exception("Scrape job failed")


def main() -> None:
    if SCRAPE_ONCE:
        job()
        return
    tz = SCHEDULE_TIMEZONE
    log.info(
        "Scheduler: daily at %02d:%02d %s",
        SCHEDULE_HOUR,
        SCHEDULE_MINUTE,
        tz,
    )
    sched = BlockingScheduler()
    sched.add_job(
        job,
        CronTrigger(
            hour=SCHEDULE_HOUR,
            minute=SCHEDULE_MINUTE,
            timezone=tz,
        ),
    )
    sched.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
