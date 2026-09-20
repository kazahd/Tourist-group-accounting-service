# tests/test_groups.py
"""Тесты функций модуля groups."""

from groups import add_group, find_group, get_group_status


def test_group_status_has_free_places():
    assert "Свободно" in get_group_status(3, 10)


def test_group_status_full():
    assert get_group_status(10, 10) == "Группа заполнена. Мест нет."


def test_add_group():
    groups = []
    add_group(groups, "Поход в горы", "Алтай", 10)
    assert len(groups) == 1
    assert groups[0]["name"] == "Поход в горы"


def test_find_group():
    groups = []
    add_group(groups, "Поход в горы", "Алтай", 10)
    assert len(find_group(groups, "горы")) == 1
