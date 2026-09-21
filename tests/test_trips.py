# tests/test_trips.py
"""Тесты класса Trip и функций."""

from models import Group, Trip
from models.trips import add_trip


def test_trip_creation():
    group = Group(1, "Поход в горы", "Алтай", 10)
    trip = Trip(1, group, "2026-07-15")
    assert trip.id == 1
    assert trip.group is group
    assert trip.trip_date == "2026-07-15"


def test_trip_str():
    group = Group(1, "Поход в горы", "Алтай", 10)
    trip = Trip(1, group, "2026-07-15")
    assert "Поход в горы" in str(trip)


def test_add_trip():
    group = Group(1, "Поход в горы", "Алтай", 10)
    trips = []
    add_trip(trips, group, "2026-07-15")
    assert len(trips) == 1
    assert isinstance(trips[0], Trip)
