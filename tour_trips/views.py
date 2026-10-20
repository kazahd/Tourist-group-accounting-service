from django.http import HttpResponse

from homepage.views import page
from models.trips import find_trip_by_id
from storage import load_groups, load_trips


def trips(request):
    """Страница списка поездок."""
    groups_list = load_groups("data/groups.json")
    trips_list = load_trips("data/trips.json", groups_list)

    items = ""
    for trip in trips_list:
        items += (
            '<li class="list-group-item d-flex justify-content-between '
            'align-items-center">'
            f'<div><a href="/trips/{trip.id}/" class="text-decoration-none">'
            f"<strong>{trip.group.name}</strong></a> — {trip.trip_date}</div>"
            '<span class="badge bg-success rounded-pill">Запланирована</span>'
            "</li>"
        )

    content = f"""
    <h1>Поездки</h1>
    <ul class="list-group mt-3">
        {items}
    </ul>
    """
    return HttpResponse(page("Поездки", content))


def trip_detail(request, trip_id):
    """Страница конкретной поездки."""
    groups_list = load_groups("data/groups.json")
    trips_list = load_trips("data/trips.json", groups_list)
    trip = find_trip_by_id(trips_list, trip_id)

    if trip is None:
        content = """
        <h1 class="text-danger">Поездка не найдена</h1>
        <a href="/trips/" class="btn btn-outline-secondary">
            ← К списку поездок
        </a>
        """
        return HttpResponse(page("Поездка не найдена", content), status=404)

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Поездка №{trip.id}</h5>
            <p class="card-text">
                <strong>Группа:</strong> {trip.group.name}
            </p>
            <p class="card-text">
                <strong>Маршрут:</strong> {trip.group.route}
            </p>
            <p class="card-text">
                <strong>Дата:</strong> {trip.trip_date}
            </p>
            <a href="/trips/" class="btn btn-outline-secondary">
                ← К списку поездок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Поездка №{trip.id}", content))
