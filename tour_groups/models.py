"""Модели предметной области: группы, участники, поездки."""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator


class Group(models.Model):
    """Туристическая группа."""

    name = models.CharField(max_length=100, verbose_name="Название")
    route = models.CharField(max_length=200, verbose_name="Маршрут")
    max_capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], verbose_name="Вместимость"
    )
    slug = models.SlugField(
        max_length=120, unique=True, blank=True, verbose_name="Адрес"
    )
    image = models.ImageField(
        upload_to="groups/", blank=True, null=True, verbose_name="Фотография"
    )

    class Meta:
        db_table = "groups"
        ordering = ["name"]
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self) -> str:
        return f"[{self.pk}] {self.name} — {self.route}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True) or "group"
            candidate = base
            suffix = 2
            while (
                Group.objects.filter(slug=candidate)
                .exclude(pk=self.pk)
                .exists()
            ):
                candidate = f"{base}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tour_groups:detail", kwargs={"slug": self.slug})

    def has_free_places(self) -> bool:
        """Есть ли свободные места (по количеству участников)."""
        return self.participants.count() < self.max_capacity


class Participant(models.Model):
    """Участник туристической группы."""

    name = models.CharField(max_length=100, verbose_name="Имя")
    age = models.PositiveIntegerField(verbose_name="Возраст")
    is_adult = models.GeneratedField(
        expression=models.Case(
            models.When(age__gte=18, then=models.Value(True)),
            default=models.Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Совершеннолетний",
    )
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
            return (
                f"[{self.pk}] {self.name}, {self.age} лет "
                f"(группа: {self.group.name})"
            )
        return f"[{self.pk}] {self.name}, {self.age} лет"


class TripQuerySet(models.QuerySet):
    """Повторно используемые фильтры расписания поездок."""

    def active(self):
        return self.filter(status=Trip.Status.ACTIVE)

    def cancelled(self):
        return self.filter(status=Trip.Status.CANCELLED)

    def completed(self):
        return self.filter(status=Trip.Status.COMPLETED)

    def for_date(self, trip_date):
        return self.filter(trip_date=trip_date)


class Trip(models.Model):
    """Поездка туристической группы."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Запланирована"
        CANCELLED = "cancelled", "Отменена"
        COMPLETED = "completed", "Завершена"

    objects = TripQuerySet.as_manager()

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="trips",
        verbose_name="Группа",
    )
    trip_date = models.DateField(verbose_name="Дата поездки")
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус",
    )

    class Meta:
        db_table = "trips"
        ordering = ["trip_date"]
        verbose_name = "Поездка"
        verbose_name_plural = "Поездки"

    def __str__(self) -> str:
        return f"[{self.pk}] {self.group.name} — {self.trip_date}"

    def cancel(self):
        """Отменяет запланированную поездку; завершенную отменить нельзя."""
        if self.status == self.Status.COMPLETED:
            return False
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])
        return True
