"""Модуль для сохранения и загрузки данных в JSON-файлах."""
import json
import os


def load_groups(filename: str) -> list[dict]:
    """Загрузить группы из JSON-файла. При отсутствии файла — пустой список."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён.")
        return []


def save_groups(filename: str, groups: list[dict]) -> None:
    """Сохранить группы в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)


def load_participants(filename: str) -> list[dict]:
    """Загрузить участников из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён.")
        return []


def save_participants(filename: str, participants: list[dict]) -> None:
    """Сохранить участников в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(participants, f, ensure_ascii=False, indent=2)
