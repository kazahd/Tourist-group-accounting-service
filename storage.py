"""Модуль для сохранения и загрузки данных в JSON-файлах."""

import json


def load_groups(filename: str) -> list[dict]:
    """Загрузить группы из JSON-файла.

    TODO: открыть файл через контекстный менеджер with,
    прочитать данные и вернуть список групп.
    Обработать отсутствие файла и некорректный JSON.
    """
    pass


def save_groups(filename: str, groups: list[dict]) -> None:
    """Сохранить группы в JSON-файл.

    TODO: записать список групп в файл
    с использованием контекстного менеджера with.
    """
    pass


def load_participants(filename: str) -> list[dict]:
    """Загрузить участников из JSON-файла.

    TODO: аналогично load_groups() - прочитать
    и вернуть список участников.
    """
    pass


def save_participants(filename: str, participants: list[dict]) -> None:
    """Сохранить участников в JSON-файл.

    TODO: записать список участников в файл.
    """
    pass