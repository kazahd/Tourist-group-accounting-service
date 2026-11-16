"""Выгружает данные из старой sqlite-БД ПР7 в JSON-фикстуры Django."""
import json
import re
import sqlite3
from pathlib import Path

OLD_DB = Path("data/tourist.sqlite")
OUT = Path("fixtures")
OUT.mkdir(exist_ok=True)


def dump(table: str, model: str, fields: list[str], filename: str) -> None:
    conn = sqlite3.connect(OLD_DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(f"SELECT * FROM {table} ORDER BY id;").fetchall()
    conn.close()

    payload = []
    used_slugs = set()
    for row in rows:
        values = {f: row[f] for f in fields}
        if model == "tour_groups.group":
            normalized_name = row["name"].strip().lower()
            normalized_name = re.sub(
                r"[^\w-]+", "-", normalized_name, flags=re.UNICODE
            ).strip("-")
            base = normalized_name or f"group-{row['id']}"
            slug = base
            suffix = 2
            while slug in used_slugs:
                slug = f"{base}-{suffix}"
                suffix += 1
            used_slugs.add(slug)
            values["slug"] = slug
        payload.append({"model": model, "pk": row["id"], "fields": values})
    with open(OUT / filename, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)
    print(f"{filename}: {len(payload)} записей")


dump(
    "groups",
    "tour_groups.group",
    ["name", "route", "max_capacity"],
    "groups.json",
)
dump(
    "participants",
    "tour_groups.participant",
    ["name", "age", "group_id"],
    "participants.json",
)
dump(
    "trips",
    "tour_groups.trip",
    ["group_id", "trip_date"],
    "trips.json",
)
