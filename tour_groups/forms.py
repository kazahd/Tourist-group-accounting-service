"""Формы сервиса: поиск, создание поездок и запись участников."""
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Group, Participant, Trip


class BootstrapFormMixin:
    """Добавляет единое оформление Bootstrap всем полям формы."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(
                field.widget, (forms.CheckboxInput, forms.RadioSelect)
            ):
                css_class = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                css_class = "form-select"
            else:
                css_class = "form-control"
            current = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{current} {css_class}".strip()


class TripFilterForm(BootstrapFormMixin, forms.Form):
    """GET-фильтр расписания поездок."""

    group = forms.CharField(required=False, label="Название группы")
    date_from = forms.DateField(
        required=False,
        label="С даты",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_to = forms.DateField(
        required=False,
        label="По дату",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    status = forms.ChoiceField(
        required=False,
        label="Статус",
        choices=[("", "Любой статус"), *Trip.Status.choices],
    )

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get("date_from"), cleaned.get("date_to")
        if start and end and start > end:
            raise ValidationError(
                "Начальная дата не может быть позже конечной."
            )
        return cleaned


class TripForm(BootstrapFormMixin, forms.ModelForm):
    """Форма создания/редактирования поездки с проверкой дубля."""

    class Meta:
        model = Trip
        fields = ("group", "trip_date", "status")
        widgets = {"trip_date": forms.DateInput(attrs={"type": "date"})}

    def clean_trip_date(self):
        trip_date = self.cleaned_data["trip_date"]
        submitted_status = self.data.get("status", Trip.Status.ACTIVE)
        if (
            trip_date < timezone.localdate()
            and submitted_status != Trip.Status.COMPLETED
        ):
            raise ValidationError(
                "Дата активной поездки не может быть в прошлом. "
                "Для завершенной поездки выберите статус «Завершена»."
            )
        return trip_date

    def clean(self):
        cleaned = super().clean()
        group, trip_date = cleaned.get("group"), cleaned.get("trip_date")
        if group and trip_date:
            duplicates = Trip.objects.active().filter(
                group=group, trip_date=trip_date
            )
            if self.instance.pk:
                duplicates = duplicates.exclude(pk=self.instance.pk)
            if duplicates.exists():
                self.add_error(
                    "trip_date",
                    "У этой группы уже запланирована поездка на эту дату.",
                )
        return cleaned


class GroupForm(BootstrapFormMixin, forms.ModelForm):
    """Форма группы с необязательной фотографией маршрута."""

    class Meta:
        model = Group
        fields = ("name", "route", "max_capacity", "image")
        widgets = {"max_capacity": forms.NumberInput(attrs={"min": 1})}

    def clean_max_capacity(self):
        capacity = self.cleaned_data["max_capacity"]
        if capacity < 1:
            raise ValidationError(
                "Вместимость группы должна быть не меньше одного места."
            )
        return capacity


class ParticipantForm(BootstrapFormMixin, forms.ModelForm):
    """Запись участника в выбранную группу с контролем вместимости."""

    class Meta:
        model = Participant
        fields = ("name", "age")
        widgets = {"age": forms.NumberInput(attrs={"min": 0})}

    def __init__(self, *args, group, **kwargs):
        self.group = group
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        existing = self.group.participants.all()
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.count() >= self.group.max_capacity:
            raise ValidationError("В группе нет свободных мест.")
        return cleaned

    def save(self, commit=True):
        participant = super().save(commit=False)
        participant.group = self.group
        if commit:
            participant.save()
        return participant
