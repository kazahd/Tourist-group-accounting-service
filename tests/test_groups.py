# tests/test_groups.py
"""Тесты классов и функций модуля groups."""

from models import Group
from models.groups import add_group, find_group


def test_group_creation():
    group = Group(1, "Поход в горы", "Алтай", 10)
    assert group.id == 1
    assert group.name == "Поход в горы"
    assert group.route == "Алтай"
    assert group.max_capacity == 10


def test_group_str():
    group = Group(1, "Поход в горы", "Алтай", 10)
    assert "Поход в горы" in str(group)


def test_group_has_free_places():
    group = Group(1, "Поход в горы", "Алтай", 10)
    assert group.has_free_places(3) is True
    assert group.has_free_places(10) is False


def test_add_group():
    groups = []
    add_group(groups, "Поход в горы", "Алтай", 10)
    assert len(groups) == 1
    assert isinstance(groups[0], Group)


def test_find_group():
    groups = []
    add_group(groups, "Поход в горы", "Алтай", 10)
    assert len(find_group(groups, "горы")) == 1
