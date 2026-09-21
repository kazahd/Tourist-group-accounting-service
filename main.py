# main.py
"""Точка запуска приложения 'Сервис учета туристических групп'."""

from typing import List

from models import Group, Participant, Trip
from models.groups import add_group, find_group, show_groups
from models.participants import (
    add_participant,
    filter_participants_by_age,
    show_participants,
)
from models.trips import add_trip, show_trips
from storage import (
    load_groups,
    load_participants,
    load_trips,
    save_groups,
    save_participants,
    save_trips,
)
from utils import input_int, input_str

GROUPS_FILE = "data/groups.json"
PARTICIPANTS_FILE = "data/participants.json"
TRIPS_FILE = "data/trips.json"


def main() -> None:
    """Главное меню приложения."""
    groups: List[Group] = load_groups(GROUPS_FILE)
    participants: List[Participant] = load_participants(PARTICIPANTS_FILE)
    trips: List[Trip] = load_trips(TRIPS_FILE, groups)

    while True:
        print("\n=== Сервис учета туристических групп ===")
        print("1. Показать группы")
        print("2. Добавить группу")
        print("3. Найти группу")
        print("4. Показать участников")
        print("5. Добавить участника")
        print("6. Фильтр участников по возрасту")
        print("7. Показать поездки")
        print("8. Добавить поездку")
        print("0. Выход")
        choice = input_str("Выберите действие: ")

        if choice == "1":
            show_groups(groups)
        elif choice == "2":
            name = input_str("Название группы: ")
            route = input_str("Маршрут: ")
            capacity = input_int("Вместимость: ")
            add_group(groups, name, route, capacity)
            save_groups(GROUPS_FILE, groups)
            print("Группа добавлена.")
        elif choice == "3":
            query = input_str("Подстрока названия: ")
            show_groups(find_group(groups, query))
        elif choice == "4":
            show_participants(participants)
        elif choice == "5":
            name = input_str("Имя участника: ")
            age = input_int("Возраст: ")
            add_participant(participants, name, age)
            save_participants(PARTICIPANTS_FILE, participants)
            print("Участник добавлен.")
        elif choice == "6":
            min_age = input_int("Минимальный возраст: ")
            show_participants(
                filter_participants_by_age(participants, min_age)
            )
        elif choice == "7":
            show_trips(trips)
        elif choice == "8":
            show_groups(groups)
            group_id = input_int("ID группы: ")
            group = next((g for g in groups if g.id == group_id), None)
            if group is None:
                print("Группа не найдена.")
                continue
            trip_date = input_str("Дата поездки: ")
            add_trip(trips, group, trip_date)
            save_trips(TRIPS_FILE, trips)
            print("Поездка добавлена.")
        elif choice == "0":
            save_groups(GROUPS_FILE, groups)
            save_participants(PARTICIPANTS_FILE, participants)
            save_trips(TRIPS_FILE, trips)
            print("Выход.")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
