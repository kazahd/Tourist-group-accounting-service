import sqlite3
from django.shortcuts import render

DB_PATH = "data/tourist.sqlite"


def trips(request):
    """Страница списка поездок (Запрос 5)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    trips_data = conn.execute("""
        SELECT t.id, t.trip_date, g.name AS group_name
        FROM trips t
        JOIN groups g ON t.group_id = g.id
        ORDER BY t.trip_date;
    """).fetchall()
    conn.close()

    return render(request, "tour_trips/trip_list.html", {"trips": trips_data})


def trip_detail(request, trip_id):
    """Страница конкретной поездки."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    trip = conn.execute("""
        SELECT t.id, t.trip_date, g.name AS group_name, g.route
        FROM trips t
        JOIN groups g ON t.group_id = g.id
        WHERE t.id = ?;
    """, (trip_id,)).fetchone()
    conn.close()

    return render(
        request,
        "tour_trips/trip_detail.html",
        {"trip": trip},
        status=404 if trip is None else 200
    )
