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
    """Добавить участника в список и вернуть его."""
    participant_id = len(participants) + 1
    participant = {
        "id": participant_id,
        "group_id": group_id,
        "name": name,
        "age": age,
    }
    participants.append(participant)
    return participant


def find_participant(participants: list[dict], name: str) -> list[dict]:
    """Найти участников по подстроке имени."""
    result = []
    for participant in participants:
        if name.lower() in participant["name"].lower():
            result.append(participant)
    return result


def filter_participants_by_age(
    participants: list[dict], min_age: int
) -> list[dict]:
    """Отобрать участников не младше min_age."""
    result = []
    for participant in participants:
        if participant["age"] >= min_age:
            result.append(participant)
    return result
