# tests/test_groups.py
"""Тесты функций модуля groups."""

from groups import get_group_status


def test_group_status_has_free_places():
    assert "Свободно" in get_group_status(3, 10)


def test_group_status_full():
    assert get_group_status(10, 10) == "Группа заполнена. Мест нет."