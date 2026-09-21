# models/participants.py
"""Класс Participant и функции работы с участниками."""

from typing import List


class Participant:
    """Участник туристической группы."""

    def __init__(
        self,
        participant_id: int,
        name: str,
        age: int,
    ) -> None:
        """Создать объект участника."""
        self.id = participant_id
        self.name = name
        self.age = age

    def is_adult(self) -> bool:
        """Проверить, является ли участник совершеннолетним."""
        return self.age >= 18

    def __str__(self) -> str:
        """Строковое представление участника."""
        return f"[{self.id}] {self.name}, {self.age} лет"


def add_participant(
    participants: List[Participant],
    name: str,
    age: int,
) -> Participant:
    """Создать участника и добавить его в коллекцию."""
    participant_id = len(participants) + 1
    participant = Participant(participant_id, name, age)
    participants.append(participant)
    return participant


def find_participant(
    participants: List[Participant], name: str
) -> List[Participant]:
    """Найти участников по подстроке имени."""
    result = []
    for participant in participants:
        if name.lower() in participant.name.lower():
            result.append(participant)
    return result


def filter_participants_by_age(
    participants: List[Participant], min_age: int
) -> List[Participant]:
    """Отобрать участников не младше min_age."""
    result = []
    for participant in participants:
        if participant.age >= min_age:
            result.append(participant)
    return result


def show_participants(participants: List[Participant]) -> None:
    """Вывести список участников."""
    if not participants:
        print("Список участников пуст.")
        return
    for participant in participants:
        print(participant)
