"""Модуль для работы с туристическими группами."""


def add_group(groups: dict, group_name: str, route: str, max_capacity: int) -> None:
    """Добавить группу в словарь groups.

    TODO: сформировать идентификатор группы
    и добавить её данные в словарь groups.
    """
    pass


def find_group(groups: dict, query: str) -> dict:
    """Найти группы по подстроке названия.

    TODO: перебрать словарь groups и отобрать группы,
    в названии которых встречается подстрока query.
    """
    pass


def check_group_capacity(groups: dict, group_id: int, min_capacity: int) -> bool:
    """Проверить вместимость группы.

    TODO: вернуть True, если вместимость группы
    не меньше значения min_capacity.
    """
    pass


def get_group_status(current: int, max_capacity: int) -> str:
    """Вернуть текстовый статус группы."""
    if current < max_capacity:
        free = max_capacity - current
        return f"Свободно {free} мест. Можно присоединиться!"
    return "Группа заполнена. Мест нет."