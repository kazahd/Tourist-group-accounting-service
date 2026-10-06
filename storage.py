# storage.py
"""Сохранение и загрузка объектов в JSON-файлах."""

import json
import os
from typing import List

from models import Group, Participant, Trip
from models.relations import (
    find_group_by_id,
    restore_participant_relations,
)


def load_groups(filename: str) -> List[Group]:
    """Загрузить группы из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [
            Group(
                item["id"],
                item["name"],
                item["route"],
                item["max_capacity"],
            )
            for item in data
        ]
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, KeyError):
        print(f"Ошибка: файл {filename} повреждён.")
        return []


def save_groups(filename: str, groups: List[Group]) -> None:
    """Сохранить группы в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = [
        {
            "id": g.id,
            "name": g.name,
            "route": g.route,
            "max_capacity": g.max_capacity,
        }
        for g in groups
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_participants(
    filename: str, groups: List[Group]
) -> List[Participant]:
    """Загрузить участников из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён.")
        return []

    participants = [
        Participant(
            item["id"],
            item["name"],
            item["age"],
            group=find_group_by_id(groups, item.get("group_id"))
            if item.get("group_id") is not None
            else None,
        )
        for item in data
    ]

    # Восстановление связей через relations.py
    participant_group_map = {
        item["id"]: item["group_id"]
        for item in data
        if item.get("group_id") is not None
    }
    restore_participant_relations(
        participants, groups, participant_group_map
    )
    return participants


def save_participants(
    filename: str, participants: List[Participant]
) -> None:
    """Сохранить участников в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = [
        {
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "group_id": p.group.id if p.group is not None else None,
        }
        for p in participants
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_trips(
    filename: str, groups: List[Group]
) -> List[Trip]:
    """Загрузить поездки из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён.")
        return []

    trips: List[Trip] = []
    for item in data:
        group = find_group_by_id(groups, item["group_id"])
        if group is not None:
            trips.append(Trip(item["id"], group, item["trip_date"]))
    return trips


def save_trips(filename: str, trips: List[Trip]) -> None:
    """Сохранить поездки в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = [
        {
            "id": t.id,
            "group_id": t.group.id,
            "trip_date": t.trip_date,
        }
        for t in trips
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
