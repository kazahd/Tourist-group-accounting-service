"""Точка запуска приложения 'Сервис учета туристических групп'."""

from datetime import date

from groups import get_group_status
from participants import can_join, check_age

# Временные данные (на ПР3 заменятся на загрузку из файлов)
group_name = "Поход в горы"
route = "Алтай"
max_capacity = 10
current_members = 3

new_participant = "Анна Иванова"
participant_age = 28

trip_date = date(2026, 7, 15)


def main() -> None:
    """Точка запуска: основной сценарий приложения."""
    print("СЕРВИС УЧЕТА ТУРИСТИЧЕСКИХ ГРУПП")

    print(f"Группа: {group_name}")
    print(f"Маршрут: {route}")
    print(f"Участников: {current_members} из {max_capacity}")
    print(f"Дата поездки: {trip_date}")
    print(f"Новый участник: {new_participant} ({participant_age} лет)")
    print(f"Проверка возраста: {check_age(participant_age)}")

    if can_join(current_members, max_capacity):
        print("Результат: Участник может быть добавлен!")
    else:
        print("Результат: Добавление невозможно - группа переполнена")

    print(f"\nСтатус группы: {get_group_status(current_members, max_capacity)}")


if __name__ == "__main__":
    main()