"""Представления групп: ORM-версия (ПР9)."""
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Max, Min, Q
from django.shortcuts import get_object_or_404, render

from .models import Group, Participant


ALLOWED_SORTS = {
    "name": "name",
    "name_desc": "-name",
    "capacity": "max_capacity",
    "capacity_desc": "-max_capacity",
    "participants": "participants_count",
}


def _page(paginator: Paginator, number):
    try:
        return paginator.page(number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def groups(request):
    """Список групп: поиск, фильтр, сортировка, пагинация, аннотирование."""
    # ORM-1: получение набора объектов
    qs = Group.objects.all()

    # ORM-14: аннотирование (участники и поездки)
    qs = qs.annotate(
        participants_count=Count("participants", distinct=True),
        trips_count=Count("trips", distinct=True),
    )

    # ORM-7, ORM-8: поиск по нескольким полям
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(
            Q(name__icontains=query) | Q(route__icontains=query)
        )

    # ORM-3: фильтр по числу
    min_capacity = request.GET.get("min_capacity", "").strip()
    if min_capacity.isdigit():
        qs = qs.filter(max_capacity__gte=int(min_capacity))
    else:
        min_capacity = ""

    # ORM-9/10: сортировка из белого списка
    sort_key = request.GET.get("sort", "name")
    qs = qs.order_by(ALLOWED_SORTS.get(sort_key, "name"))

    # ORM-15: пагинация
    page_obj = _page(Paginator(qs, 10), request.GET.get("page", 1))

    return render(request, "tour_groups/group_list.html", {
        "groups": page_obj,
        "page_obj": page_obj,
        "query": query,
        "sort_key": sort_key,
        "min_capacity": min_capacity,
    })


def group_stats(request):
    """Статистика: аннотирование, исключение, агрегирование."""
    # ORM-14: annotate по связанной модели
    qs = Group.objects.annotate(
        participants_count=Count("participants"),
    )

    # ORM-6: exclude (убираем группы без участников)
    qs = qs.exclude(participants_count=0)

    # ORM-10: сортировка по аннотированному полю
    qs = qs.order_by("-participants_count", "name")

    # ORM-13: aggregate по всей таблице участников
    summary = Participant.objects.aggregate(
        avg_age=Avg("age"),
        max_age=Max("age"),
        min_age=Min("age"),
    )

    return render(request, "tour_groups/group_stats.html", {
        "stats": qs,
        "summary": summary,
    })


def group_detail(request, group_id):
    """Карточка группы: get по pk + related_name + select_related."""
    # ORM-2: получение одного объекта (404 автоматически)
    group = get_object_or_404(Group, pk=group_id)

    # ORM-11: обращение через related_name
    participants = group.participants.all()

    # ORM-12: select_related для поездок группы
    trips = group.trips.select_related("group").order_by("-trip_date")

    return render(request, "tour_groups/group_detail.html", {
        "group": group,
        "participants": participants,
        "trips": trips,
    })
