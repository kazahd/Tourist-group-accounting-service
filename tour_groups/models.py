"""Модели предметной области: группы, участники, поездки."""
from django.db import models


class Group(models.Model):
    """Туристическая группа."""

    name = models.CharField(max_length=100, verbose_name="Название")
    route = models.CharField(max_length=200, verbose_name="Маршрут")
    max_capacity = models.PositiveIntegerField(verbose_name="Вместимость")

    class Meta:
        db_table = "groups"
        ordering = ["name"]
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self) -> str:
        return f"[{self.pk}] {self.name} — {self.route}"

    def has_free_places(self) -> bool:
        """Есть ли свободные места (по количеству участников)."""
        return self.participants.count() < self.max_capacity


class Participant(models.Model):
    """Участник туристической группы."""

    name = models.CharField(max_length=100, verbose_name="Имя")
    age = models.PositiveIntegerField(verbose_name="Возраст")
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="participants",
        verbose_name="Группа",
    )

    class Meta:
        db_table = "participants"
        ordering = ["name"]
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    def __str__(self) -> str:
        if self.group_id:
            return f"[{self.pk}] {self.name}, {self.age} лет (группа: {self.group.name})"
        return f"[{self.pk}] {self.name}, {self.age} лет"

    def is_adult(self) -> bool:
        return self.age >= 18


class Trip(models.Model):
    """Поездка туристической группы."""

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="trips",
        verbose_name="Группа",
    )
    trip_date = models.DateField(verbose_name="Дата поездки")

    class Meta:
        db_table = "trips"
        ordering = ["trip_date"]
        verbose_name = "Поездка"
        verbose_name_plural = "Поездки"

    def __str__(self) -> str:
        return f"[{self.pk}] {self.group.name} — {self.trip_date}"
    