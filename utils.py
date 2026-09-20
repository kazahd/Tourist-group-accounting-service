"""Вспомогательные функции для ввода данных."""

from datetime import date


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число с повторным вводом при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        try:
            parts = input(prompt).split(".")
            return date(int(parts[2]), int(parts[1]), int(parts[0]))
        except (ValueError, IndexError):
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ.")


def input_str(prompt: str) -> str:
    """Запросить у пользователя непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: строка не может быть пустой.")
