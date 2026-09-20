# tests/test_participants.py
"""Тесты функций модуля participants."""

from participants import can_join, check_age


def test_can_join_true():
    assert can_join(3, 10) is True


def test_can_join_false():
    assert can_join(10, 10) is False


def test_check_age_adult():
    assert check_age(28) == "Возраст подходит"


def test_check_age_minor():
    assert check_age(15) == "Требуется разрешение родителей"