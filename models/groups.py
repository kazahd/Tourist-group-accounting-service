# models/groups.py
"""Класс Group и функции работы с группами."""

from typing import List


class Group:
    """Туристическая группа."""

    def __init__(
        self,
        group_id: int,
        name: str,
        route: str,
        max_capacity: int,
    ) -> None:
        """Создать объект группы."""
        self.id = group_id
        self.name = name
        self.route = route
        self.max_capacity = max_capacity

    def has_free_places(self, current_members: int) -> bool:
        """Проверить, есть ли свободные места в группе."""
        return current_members < self.max_capacity

    def __str__(self) -> str:
        """Строковое представление группы."""
        return f"[{self.id}] {self.name} — {self.route} " \
               f"(вместимость: {self.max_capacity})"


def add_group(
    groups: List[Group],
    name: str,
    route: str,
    max_capacity: int,
) -> Group:
    """Создать группу и добавить её в коллекцию."""
    group_id = len(groups) + 1
    group = Group(group_id, name, route, max_capacity)
    groups.append(group)
    return group


def find_group(groups: List[Group], query: str) -> List[Group]:
    """Найти группы по подстроке названия."""
    result = []
    for group in groups:
        if query.lower() in group.name.lower():
            result.append(group)
    return result


def show_groups(groups: List[Group]) -> None:
    """Вывести список групп."""
    if not groups:
        print("Список групп пуст.")
        return
    for group in groups:
        print(group)
