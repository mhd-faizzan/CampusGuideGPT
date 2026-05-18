import json
import os
import logging
import fcntl
from datetime import date

logger = logging.getLogger(__name__)

COUNTER_FILE = "usage_counter.json"

def _load(f) -> dict:
    content = f.read()
    if not content:
        return {"date": str(date.today()), "count": 0}
    return json.loads(content)

def _save(f, data: dict) -> None:
    f.seek(0)
    f.truncate()
    json.dump(data, f)

def is_limit_reached(daily_limit: int) -> bool:
    with open(COUNTER_FILE, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        data = _load(f)

        if data["date"] != str(date.today()):
            data = {"date": str(date.today()), "count": 0}
            _save(f, data)

        fcntl.flock(f, fcntl.LOCK_UN)
        return data["count"] >= daily_limit

def increment() -> None:
    with open(COUNTER_FILE, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        data = _load(f)

        if data["date"] != str(date.today()):
            data = {"date": str(date.today()), "count": 0}

        data["count"] += 1
        _save(f, data)
        fcntl.flock(f, fcntl.LOCK_UN)
        logger.info("global usage today: %d", data["count"])