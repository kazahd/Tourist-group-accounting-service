# models/trips.py
"""Класс Trip и функции работы с поездками."""

from typing import List

from .groups import Group


class Trip:
    """Поездка туристической группы."""

    def __init__(
        self,
        trip_id: int,
        group: Group,
        trip_date: str,
    ) -> None:
        """Создать объект поездки."""
        self.id = trip_id
        self.group = group
        self.trip_date = trip_date

    def __str__(self) -> str:
        """Строковое представление поездки."""
        return f"[{self.id}] {self.group.name} — {self.trip_date}"


def add_trip(
    trips: List[Trip],
    group: Group,
    trip_date: str,
) -> Trip:
    """Создать поездку и добавить её в коллекцию."""
    trip_id = len(trips) + 1
    trip = Trip(trip_id, group, trip_date)
    trips.append(trip)
    return trip


def show_trips(trips: List[Trip]) -> None:
    """Вывести список поездок."""
    if not trips:
        print("Список поездок пуст.")
        return
    for trip in trips:
        print(trip)
