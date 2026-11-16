"""Представления групп: ORM-версия (ПР9)."""
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, F, Max, Min, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import GroupForm, ParticipantForm
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
        group_name=F("name"),
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
    filter_params = request.GET.copy()
    filter_params.pop("page", None)

    return render(request, "tour_groups/group_list.html", {
        "groups": page_obj,
        "page_obj": page_obj,
        "query": query,
        "sort_key": sort_key,
        "min_capacity": min_capacity,
        "filter_query": filter_params.urlencode(),
    })


def group_stats(request):
    """Статистика: аннотирование, исключение, агрегирование."""
    # ORM-14: annotate по связанной модели
    qs = Group.objects.annotate(
        participants_count=Count("participants"),
    )

    # ORM-6: exclude (убираем группы без участников)
    qs = qs.exclude(participants_count=0).exclude(max_capacity__lt=1)

    # ORM-10: сортировка по аннотированному полю
    qs = qs.order_by("-participants_count", "name")
    qs = qs.values("id", "name", "route", "participants_count")

    # ORM-13: aggregate по всей таблице участников
    summary = Participant.objects.aggregate(
        avg_age=Avg("age"),
        max_age=Max("age"),
        min_age=Min("age"),
    )

    empty_groups = Group.objects.filter(
        participants__isnull=True
    ).values_list("name", flat=True)

    return render(request, "tour_groups/group_stats.html", {
        "stats": qs,
        "summary": summary,
        "empty_groups": empty_groups,
    })


def group_detail(request, slug):
    """Карточка группы: get по pk + related_name + select_related."""
    # ORM-2: получение одного объекта (404 автоматически)
    group = get_object_or_404(Group, slug=slug)

    # ORM-11: обращение через related_name
    participants = group.participants.all()

    # ORM-12: select_related для поездок группы
    trips = group.trips.select_related("group").order_by("-trip_date")

    return render(request, "tour_groups/group_detail.html", {
        "group": group,
        "participants": participants,
        "trips": trips,
    })


def group_create(request):
    form = GroupForm(
        request.POST if request.method == "POST" else None,
        request.FILES if request.method == "POST" else None,
    )
    if request.method == "POST" and form.is_valid():
        group = form.save()
        return redirect(group.get_absolute_url())
    return render(request, "tour_groups/group_form.html", {"form": form})


def participant_add(request, slug):
    group = get_object_or_404(Group, slug=slug)
    form = ParticipantForm(
        request.POST if request.method == "POST" else None,
        group=group,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(group.get_absolute_url())
    return render(request, "tour_groups/participant_form.html", {
        "form": form,
        "group": group,
        "remaining_places": max(
            group.max_capacity - group.participants.count(), 0
        ),
    })


@require_POST
def participant_remove(request, slug, participant_id):
    """Удаляет участника только из его группы через POST-запрос."""
    group = get_object_or_404(Group, slug=slug)
    participant = get_object_or_404(
        Participant, pk=participant_id, group=group
    )
    participant.delete()
    return redirect(group.get_absolute_url())
