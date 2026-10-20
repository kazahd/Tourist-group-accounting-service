from django.shortcuts import render

from models.groups import find_group_by_id
from storage import load_groups


def groups(request):
    """Страница списка групп."""
    groups_list = load_groups("data/groups.json")

    context = {
        "groups": groups_list,
    }
    return render(request, "tour_groups/group_list.html", context)


def group_detail(request, group_id):
    """Страница конкретной группы."""
    groups_list = load_groups("data/groups.json")
    group = find_group_by_id(groups_list, group_id)

    context = {
        "group": group,
    }

    return render(
        request,
        "tour_groups/group_detail.html",
        context,
        status=404 if group is None else 200,
    )
