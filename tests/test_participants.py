# tests/test_participants.py
"""Тесты функций модуля participants."""

from participants import (
    add_participant,
    can_join,
    check_age,
    filter_participants_by_age,
)


def test_can_join_true():
    assert can_join(3, 10) is True


def test_can_join_false():
    assert can_join(10, 10) is False


def test_check_age_adult():
    assert check_age(28) == "Возраст подходит"


def test_check_age_minor():
    assert check_age(15) == "Требуется разрешение родителей"


def test_add_participant():
    participants = []
    add_participant(participants, 1, "Анна", 28)
    assert len(participants) == 1


def test_filter_participants_by_age():
    participants = []
    add_participant(participants, 1, "Анна", 28)
    add_participant(participants, 1, "Игорь", 15)
    assert len(filter_participants_by_age(participants, 18)) == 1
