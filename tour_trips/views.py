from django.shortcuts import render

from models.trips import find_trip_by_id
from storage import load_groups, load_trips


def trips(request):
    """Страница списка поездок."""
    groups_list = load_groups("data/groups.json")
    trips_list = load_trips("data/trips.json", groups_list)

    context = {
        "trips": trips_list,
    }
    return render(request, "tour_trips/trip_list.html", context)


def trip_detail(request, trip_id):
    """Страница конкретной поездки."""
    groups_list = load_groups("data/groups.json")
    trips_list = load_trips("data/trips.json", groups_list)
    trip = find_trip_by_id(trips_list, trip_id)

    context = {
        "trip": trip,
    }

    return render(
        request,
        "tour_trips/trip_detail.html",
        context,
        status=404 if trip is None else 200,
    )
