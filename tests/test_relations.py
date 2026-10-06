# tests/test_relations.py
"""Тесты связей между сущностями."""

from models import Group, Participant
from models.relations import (
    get_participants_of_group,
    link_participant_to_group,
    unlink_participant_from_group,
)


def test_link_participant_to_group():
    group = Group(1, "Поход в горы", "Алтай", 10)
    participant = Participant(1, "Анна", 28)
    link_participant_to_group(participant, group)
    assert participant.group is group


def test_unlink_participant():
    group = Group(1, "Поход в горы", "Алтай", 10)
    participant = Participant(1, "Анна", 28)
    link_participant_to_group(participant, group)
    unlink_participant_from_group(participant)
    assert participant.group is None


def test_get_participants_of_group():
    group = Group(1, "Поход в горы", "Алтай", 10)
    p1 = Participant(1, "Анна", 28)
    p2 = Participant(2, "Игорь", 30)
    link_participant_to_group(p1, group)
    link_participant_to_group(p2, group)
    result = get_participants_of_group([p1, p2], group)
    assert len(result) == 2
