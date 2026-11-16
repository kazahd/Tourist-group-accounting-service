"""Настройка административной панели сервиса."""
from django.contrib import admin
from django.utils.html import format_html

from .models import Group, Participant, Trip


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0
    fields = ("name", "age")
    show_change_link = True


class TripInline(admin.TabularInline):
    model = Trip
    extra = 0
    fields = ("trip_date", "status")
    show_change_link = True


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name", "route", "max_capacity", "slug", "image_preview",
        "participant_total", "trip_total",
    )
    search_fields = ("name", "route", "slug")
    list_filter = ("max_capacity",)
    ordering = ("name",)
    list_per_page = 25
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("image_preview",)
    inlines = (ParticipantInline, TripInline)

    @admin.display(description="Фото")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank">Открыть фото</a>', obj.image.url
            )
        return "—"

    @admin.display(description="Участники")
    def participant_total(self, obj):
        return obj.participant_count

    @admin.display(description="Поездки")
    def trip_total(self, obj):
        return obj.trip_count

    def get_queryset(self, request):
        from django.db.models import Count
        return super().get_queryset(request).annotate(
            participant_count=Count("participants", distinct=True),
            trip_count=Count("trips", distinct=True),
        )


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "is_adult", "group")
    readonly_fields = ("is_adult",)
    list_filter = ("age", "group")
    search_fields = ("name", "group__name")
    autocomplete_fields = ("group",)
    ordering = ("name",)
    list_per_page = 25


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("group", "trip_date", "status")
    list_filter = ("status", "trip_date")
    search_fields = ("group__name", "group__route")
    autocomplete_fields = ("group",)
    ordering = ("-trip_date",)
    list_per_page = 25
