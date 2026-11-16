"""Представления поездок: ORM-версия (ПР9)."""
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render

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

    # ORM-5: фильтр по полю связанной модели
    group_query = request.GET.get("group", "").strip()
    if group_query:
        qs = qs.filter(group__name__icontains=group_query)

    # ORM-4: фильтр по диапазону дат
    date_from = request.GET.get("from", "").strip()
    date_to = request.GET.get("to", "").strip()
    if date_from:
        qs = qs.filter(trip_date__gte=date_from)
    if date_to:
        qs = qs.filter(trip_date__lte=date_to)

    # ORM-10: сортировка из белого списка
    sort_key = request.GET.get("sort", "date")
    qs = qs.order_by(ALLOWED_SORTS.get(sort_key, "trip_date"))

    # ORM-15: пагинация
    page_obj = _page(Paginator(qs, 10), request.GET.get("page", 1))

    return render(request, "tour_trips/trip_list.html", {
        "trips": page_obj,
        "page_obj": page_obj,
        "group_query": group_query,
        "sort_key": sort_key,
        "date_from": date_from,
        "date_to": date_to,
    })


def trip_detail(request, trip_id):
    """Карточка поездки: ORM-2 + select_related."""
    trip = get_object_or_404(
        Trip.objects.select_related("group"), pk=trip_id
    )
    return render(request, "tour_trips/trip_detail.html", {"trip": trip})
