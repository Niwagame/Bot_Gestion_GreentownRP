# limits.py
from datetime import datetime, timedelta
from typing import Tuple

from db import fetchone, fetchall, execute


def humandelta(until: datetime) -> str:
    """Formatte un delta 'humain' (ex: 1h 23m)."""
    delta = until - datetime.now()
    secs = max(0, int(delta.total_seconds()))
    d, r = divmod(secs, 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    parts = []
    if d:
        parts.append(f"{d}j")
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}m")
    if not parts:
        parts.append(f"{s}s")
    return " ".join(parts)


def check_and_set_global_cooldown(action: str, cooldown_min: int) -> Tuple[bool, datetime]:
    """
    Renvoie (True, nouvelle_dispo) si le cooldown est OK et qu'on vient de le poser.
            (False, dispo_existante) si encore en cooldown.
    """
    now = datetime.now()
    row = fetchone("SELECT available_at FROM GlobalCooldowns WHERE action=%s", (action,))
    if row and now < row["available_at"]:
        return False, row["available_at"]

    available_at = now + timedelta(minutes=cooldown_min)
    execute(
        "REPLACE INTO GlobalCooldowns(action, available_at) VALUES (%s,%s)",
        (action, available_at),
    )
    return True, available_at


def increment_group_daily(action: str, group_name: str, limit_per_day: int) -> Tuple[bool, int]:
    """
    Incrémente le compteur du jour pour (action, group_name).
    Renvoie (True, nouveau_compteur) si autorisé, (False, compteur_actuel) sinon.
    """
    today = datetime.now().date()
    row = fetchone(
        "SELECT count FROM GroupDailyCounts WHERE action=%s AND group_name=%s AND day=%s",
        (action, group_name, today),
    )
    count = row["count"] if row else 0
    if count >= limit_per_day:
        return False, count

    if row:
        execute(
            "UPDATE GroupDailyCounts SET count = count + 1 WHERE action=%s AND group_name=%s AND day=%s",
            (action, group_name, today),
        )
        return True, count + 1

    execute(
        "INSERT INTO GroupDailyCounts(action, group_name, day, count) VALUES (%s,%s,%s,1)",
        (action, group_name, today),
    )
    return True, 1


def active_count(action: str, group_name: str) -> int:
    rows = fetchall(
        "SELECT 1 FROM ActiveActivities WHERE action=%s AND group_name=%s AND ends_at > %s",
        (action, group_name, datetime.now()),
    )
    return len(rows)


def start_active(action: str, group_name: str, duration_min: float) -> datetime:
    now = datetime.now()
    ends = now + timedelta(minutes=duration_min)
    execute(
        "INSERT INTO ActiveActivities(action, group_name, started_at, ends_at) VALUES (%s,%s,%s,%s)",
        (action, group_name, now, ends),
    )
    return ends


def end_active_cleanup(action: str, group_name: str) -> None:
    execute(
        "DELETE FROM ActiveActivities WHERE action=%s AND group_name=%s AND ends_at <= %s",
        (action, group_name, datetime.now()),
    )
