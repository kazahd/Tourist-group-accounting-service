"""Выгружает данные из старой sqlite-БД ПР7 в JSON-фикстуры Django."""
import json
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

    payload = [
        {
            "model": model,
            "pk": row["id"],
            "fields": {f: row[f] for f in fields},
        }
        for row in rows
    ]
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
