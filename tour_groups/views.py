import sqlite3

from django.shortcuts import render

DB_PATH = "data/tourist.sqlite"


def groups(request):
    """Страница списка групп (Запрос 1)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    groups_data = conn.execute(
        "SELECT id, name, route, max_capacity FROM groups ORDER BY name;"
    ).fetchall()
    conn.close()

    return render(
        request,
        "tour_groups/group_list.html",
        {"groups": groups_data},
    )


def group_stats(request):
    """Страница статистики групп (Запрос 8)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    stats = conn.execute("""
        SELECT g.name AS group_name, COUNT(p.id) AS participants_count
        FROM groups g
        LEFT JOIN participants p ON g.id = p.group_id
        GROUP BY g.id, g.name;
    """).fetchall()
    conn.close()

    return render(
        request,
        "tour_groups/group_stats.html",
        {"stats": stats},
    )
