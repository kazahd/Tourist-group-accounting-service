from django.urls import path
from . import views

app_name = "tour_groups"

urlpatterns = [
    path("", views.groups, name="list"),
    path("stats/", views.group_stats, name="stats"),
    path("create/", views.group_create, name="create"),
    path(
        "<str:slug>/participants/add/",
        views.participant_add,
        name="participant_add",
    ),
    path(
        "<str:slug>/participants/<int:participant_id>/remove/",
        views.participant_remove,
        name="participant_remove",
    ),
    # str accepts Unicode slugs produced from Russian group names.
    path("<str:slug>/", views.group_detail, name="detail"),
]
