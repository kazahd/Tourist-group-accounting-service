from django.urls import path
from . import views

app_name = "tour_trips"

urlpatterns = [
    path("", views.trips, name="list"),
    path("create/", views.trip_create, name="create"),
    path("<int:trip_id>/edit/", views.trip_update, name="update"),
    path("<int:trip_id>/cancel/", views.trip_cancel, name="cancel"),
    path("<int:trip_id>/", views.trip_detail, name="detail"),
]
