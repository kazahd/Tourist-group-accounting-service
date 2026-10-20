import json
from db.database import get_connection

GROUPS_FILE = "data/groups.json"
PARTICIPANTS_FILE = "data/participants.json"
TRIPS_FILE = "data/trips.json"


def load_json(filename):
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def import_data():
    conn = get_connection()
    try:
        # Импорт групп
        groups = load_json(GROUPS_FILE)
        conn.executemany(
            "INSERT OR IGNORE INTO groups (id, name, route, max_capacity) "
            "VALUES (?, ?, ?, ?)",
            [
                (g["id"], g["name"], g["route"], g["max_capacity"])
                for g in groups
            ],
        )

        # Импорт участников
        participants = load_json(PARTICIPANTS_FILE)
        conn.executemany(
            "INSERT OR IGNORE INTO participants (id, name, age, group_id) "
            "VALUES (?, ?, ?, ?)",
            [
                (p["id"], p["name"], p["age"], p.get("group_id"))
                for p in participants
            ],
        )

        # Импорт поездок
        trips = load_json(TRIPS_FILE)
        conn.executemany(
            "INSERT OR IGNORE INTO trips (id, group_id, trip_date) "
            "VALUES (?, ?, ?)",
            [(t["id"], t["group_id"], t["trip_date"]) for t in trips],
        )

        conn.commit()
        print("Данные успешно импортированы.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при импорте: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    import_data()
