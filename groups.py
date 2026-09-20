"""Модуль для работы с туристическими группами."""


def add_group(groups: list[dict], name: str, route: str,
              max_capacity: int) -> dict:
    """Добавить группу в список и вернуть её."""
    group_id = len(groups) + 1
    group = {
        "id": group_id,
        "name": name,
        "route": route,
        "max_capacity": max_capacity,
    }
    groups.append(group)
    return group


def find_group(groups: list[dict], query: str) -> list[dict]:
    """Найти группы по подстроке названия."""
    result = []
    for group in groups:
        if query.lower() in group["name"].lower():
            result.append(group)
    return result


def check_group_capacity(groups: list[dict], group_id: int,
                         min_capacity: int) -> bool:
    """Проверить, что вместимость группы не меньше min_capacity."""
    for group in groups:
        if group["id"] == group_id:
            return group["max_capacity"] >= min_capacity
    return False


def get_group_status(current: int, max_capacity: int) -> str:
    """Вернуть текстовый статус группы."""
    if current < max_capacity:
        free = max_capacity - current
        return f"Свободно {free} мест. Можно присоединиться!"
    return "Группа заполнена. Мест нет."
