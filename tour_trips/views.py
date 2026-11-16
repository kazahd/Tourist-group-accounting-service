"""Представления поездок: ORM-версия (ПР9)."""
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from tour_groups.forms import TripFilterForm, TripForm
from tour_groups.models import Trip


ALLOWED_SORTS = {
    "date": "trip_date",
    "date_desc": "-trip_date",
    "group": "group__name",
}


def _page(paginator, number):
    try:
        return paginator.page(number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def trips(request):
    """Список поездок: select_related, фильтры, сортировка, пагинация."""
    # ORM-12: select_related заменяет JOIN из Запроса 5
    qs = Trip.objects.select_related("group").all()
    filter_data = request.GET.copy()
    if "date_from" not in filter_data and "from" in filter_data:
        filter_data["date_from"] = filter_data["from"]
    if "date_to" not in filter_data and "to" in filter_data:
        filter_data["date_to"] = filter_data["to"]
    filter_form = TripFilterForm(filter_data)
    if filter_form.is_valid():
        filters = filter_form.cleaned_data
        status = filters["status"]
        if status:
            # Используем именованные методы QuerySet из PR10.
            status_filters = {
                Trip.Status.ACTIVE: Trip.objects.active,
                Trip.Status.CANCELLED: Trip.objects.cancelled,
                Trip.Status.COMPLETED: Trip.objects.completed,
            }
            qs = status_filters[status]().select_related("group")
        group_query = filters["group"].strip()
        if group_query:
            qs = qs.filter(group__name__icontains=group_query)
        if filters["date_from"]:
            qs = qs.filter(trip_date__gte=filters["date_from"])
        if filters["date_to"]:
            qs = qs.filter(trip_date__lte=filters["date_to"])
    else:
        group_query = ""
        status = ""

    # ORM-10: сортировка из белого списка
    sort_key = request.GET.get("sort", "date")
    qs = qs.order_by(ALLOWED_SORTS.get(sort_key, "trip_date"))

    # ORM-15: пагинация
    page_obj = _page(Paginator(qs, 10), request.GET.get("page", 1))

    return render(request, "tour_trips/trip_list.html", {
        "trips": page_obj,
        "page_obj": page_obj,
        "filter_form": filter_form,
        "group_query": group_query,
        "sort_key": sort_key,
        "status": status,
        "filter_query": _filter_query(request),
    })


def _filter_query(request):
    query = request.GET.copy()
    query.pop("page", None)
    return query.urlencode()


def _trip_form(request, instance=None):
    form = TripForm(
        request.POST if request.method == "POST" else None,
        instance=instance,
    )
    if request.method == "POST" and form.is_valid():
        trip = form.save()
        return redirect("tour_trips:detail", trip_id=trip.pk)
    return render(
        request,
        "tour_trips/trip_form.html",
        {"form": form, "trip": instance},
    )


def trip_create(request):
    return _trip_form(request)


def trip_update(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    return _trip_form(request, instance=trip)


@require_POST
def trip_cancel(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    trip.cancel()
    return redirect("tour_trips:detail", trip_id=trip.pk)


def trip_detail(request, trip_id):
    """Карточка поездки: ORM-2 + select_related."""
    trip = get_object_or_404(
        Trip.objects.select_related("group"), pk=trip_id
    )
    return render(request, "tour_trips/trip_detail.html", {
        "trip": trip,
        "can_cancel": trip.status not in (
            Trip.Status.COMPLETED,
            Trip.Status.CANCELLED,
        ),
    })
