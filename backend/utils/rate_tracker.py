import json
import os
import logging
from datetime import date

logger = logging.getLogger(__name__)

COUNTER_FILE = "usage_counter.json"

def _load() -> dict:
    if not os.path.exists(COUNTER_FILE):
        return {"date": str(date.today()), "count": 0}
    with open(COUNTER_FILE, "r") as f:
        return json.load(f)

def _save(data: dict) -> None:
    with open(COUNTER_FILE, "w") as f:
        json.dump(data, f)

def is_limit_reached(daily_limit: int) -> bool:
    data = _load()

    # reset counter if it's a new day
    if data["date"] != str(date.today()):
        data = {"date": str(date.today()), "count": 0}
        _save(data)

    return data["count"] >= daily_limit

def increment() -> None:
    data = _load()

    # reset if new day
    if data["date"] != str(date.today()):
        data = {"date": str(date.today()), "count": 0}

    data["count"] += 1
    _save(data)
    logger.info("global usage today: %d", data["count"])