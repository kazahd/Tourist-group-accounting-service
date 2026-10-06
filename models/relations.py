# models/relations.py
"""Единый модуль связей между сущностями предметной области."""

from typing import List, Optional

from .groups import Group
from .participants import Participant
from .trips import Trip


def link_participant_to_group(
    participant: Participant,
    group: Group,
) -> None:
    """Связать участника с группой."""
    participant.group = group


def unlink_participant_from_group(participant: Participant) -> None:
    """Отвязать участника от группы."""
    participant.group = None


def find_group_by_id(
    groups: List[Group],
    group_id: int,
) -> Optional[Group]:
    """Найти группу по идентификатору."""
    for group in groups:
        if group.id == group_id:
            return group
    return None


def find_participant_by_id(
    participants: List[Participant],
    participant_id: int,
) -> Optional[Participant]:
    """Найти участника по идентификатору."""
    for participant in participants:
        if participant.id == participant_id:
            return participant
    return None


def restore_trip_relations(
    trips: List[Trip],
    groups: List[Group],
) -> None:
    """Восстановить связи Trip → Group для всех поездок.

    Используется при загрузке из JSON: в файле хранится только group_id.
    """
    for trip in trips:
        if trip.group is not None:
            continue
        # заглушка, если group не был передан ранее
        trip.group = find_group_by_id(groups, trip.group.id) or trip.group


def restore_participant_relations(
    participants: List[Participant],
    groups: List[Group],
    participant_group_map: dict,
) -> None:
    """Восстановить связи Participant → Group при загрузке.

    participant_group_map: {participant_id: group_id}
    """
    for participant in participants:
        group_id = participant_group_map.get(participant.id)
        if group_id is not None:
            group = find_group_by_id(groups, group_id)
            if group is not None:
                participant.group = group


def get_participants_of_group(
    participants: List[Participant],
    group: Group,
) -> List[Participant]:
    """Получить всех участников указанной группы."""
    return [p for p in participants if p.group is group]


def get_trips_of_group(
    trips: List[Trip],
    group: Group,
) -> List[Trip]:
    """Получить все поездки указанной группы."""
    return [t for t in trips if t.group is group]
