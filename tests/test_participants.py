# tests/test_participants.py
"""Тесты класса Participant и функций."""

from models import Participant
from models.participants import (
    add_participant,
    filter_participants_by_age,
    find_participant,
)


def test_participant_creation():
    p = Participant(1, "Анна Иванова", 28)
    assert p.id == 1
    assert p.name == "Анна Иванова"
    assert p.age == 28


def test_participant_is_adult():
    assert Participant(1, "Анна", 28).is_adult() is True
    assert Participant(2, "Игорь", 15).is_adult() is False


def test_add_participant():
    participants = []
    add_participant(participants, "Анна", 28)
    assert len(participants) == 1
    assert isinstance(participants[0], Participant)


def test_find_participant():
    participants = []
    add_participant(participants, "Анна Иванова", 28)
    assert len(find_participant(participants, "Анна")) == 1


def test_filter_participants_by_age():
    participants = []
    add_participant(participants, "Анна", 28)
    add_participant(participants, "Игорь", 15)
    assert len(filter_participants_by_age(participants, 18)) == 1
