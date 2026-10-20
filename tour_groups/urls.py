from django.urls import path
from . import views

app_name = "tour_groups"

urlpatterns = [
    path("", views.groups, name="list"),
    path("stats/", views.group_stats, name="stats"),
]
