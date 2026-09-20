"""Точка запуска приложения 'Сервис учета туристических групп'."""

from groups import add_group, find_group
from participants import add_participant, check_age, filter_participants_by_age
from storage import (
    load_groups,
    load_participants,
    save_groups,
    save_participants,
)
from utils import input_int, input_str

GROUPS_FILE = "data/groups.json"
PARTICIPANTS_FILE = "data/participants.json"


def show_groups(groups: list[dict]) -> None:
    """Вывести список групп."""
    if not groups:
        print("Список групп пуст.")
        return
    for group in groups:
        print(f"[{group['id']}] {group['name']} — "
              f"{group['route']} (вместимость: {group['max_capacity']})")


def show_participants(participants: list[dict]) -> None:
    """Вывести список участников."""
    if not participants:
        print("Список участников пуст.")
        return
    for p in participants:
        print(f"[{p['id']}] {p['name']}, {p['age']} лет, "
              f"группа {p['group_id']}")


def main() -> None:
    """Главное меню приложения."""
    groups = load_groups(GROUPS_FILE)
    participants = load_participants(PARTICIPANTS_FILE)

    while True:
        print("\n=== Сервис учета туристических групп ===")
        print("1. Показать группы")
        print("2. Добавить группу")
        print("3. Найти группу")
        print("4. Показать участников")
        print("5. Добавить участника")
        print("6. Фильтр участников по возрасту")
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
            found = find_group(groups, query)
            show_groups(found)
        elif choice == "4":
            show_participants(participants)
        elif choice == "5":
            show_groups(groups)
            group_id = input_int("ID группы: ")
            name = input_str("Имя участника: ")
            age = input_int("Возраст: ")
            print(check_age(age))
            add_participant(participants, group_id, name, age)
            save_participants(PARTICIPANTS_FILE, participants)
            print("Участник добавлен.")
        elif choice == "6":
            min_age = input_int("Минимальный возраст: ")
            found = filter_participants_by_age(participants, min_age)
            show_participants(found)
        elif choice == "0":
            save_groups(GROUPS_FILE, groups)
            save_participants(PARTICIPANTS_FILE, participants)
            print("Выход.")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
