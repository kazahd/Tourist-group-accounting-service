"""Модуль для работы с участниками туристических групп."""


def can_join(current: int, max_capacity: int) -> bool:
    """Проверить, можно ли добавить участника в группу."""
    return current < max_capacity


def check_age(age: int) -> str:
    """Проверить возраст участника."""
    if age >= 18:
        return "Возраст подходит"
    return "Требуется разрешение родителей"


def add_participant(
    participants: list[dict], group_id: int, name: str, age: int
) -> dict:
    """Добавить участника в группу.

    TODO: сформировать словарь участника
    и добавить его в список participants.
    """
    pass


def find_participant(participants: list[dict], name: str) -> list[dict]:
    """Найти участников по имени.

    TODO: перебрать список participants и отобрать участников,
    в имени которых встречается подстрока name.
    """
    pass


def filter_participants_by_age(participants: list[dict], min_age: int) -> list[dict]:
    """Отобрать участников по возрасту.

    TODO: перебрать список participants и вернуть участников
    не младше min_age лет.
    """
    pass