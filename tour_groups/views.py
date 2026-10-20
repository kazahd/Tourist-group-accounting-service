from django.http import HttpResponse

from homepage.views import page
from models.groups import find_group_by_id
from storage import load_groups


def groups(request):
    """Страница списка групп."""
    groups_list = load_groups("data/groups.json")

    items = ""
    for group in groups_list:
        items += (
            '<li class="list-group-item d-flex justify-content-between '
            'align-items-center">'
            f'<div><a href="/groups/{group.id}/" class="text-decoration-none">'
            f"<strong>{group.name}</strong></a> (Маршрут: {group.route})</div>"
            f'<span class="badge bg-primary rounded-pill">'
            f"до {group.max_capacity} чел.</span>"
            "</li>"
        )

    content = f"""
    <h1>Туристические группы</h1>
    <ul class="list-group mt-3">
        {items}
    </ul>
    """
    return HttpResponse(page("Группы", content))


def group_detail(request, group_id):
    """Страница конкретной группы."""
    groups_list = load_groups("data/groups.json")
    group = find_group_by_id(groups_list, group_id)

    if group is None:
        content = """
        <h1 class="text-danger">Группа не найдена</h1>
        <a href="/groups/" class="btn btn-outline-secondary">
            ← К списку групп
        </a>
        """
        return HttpResponse(page("Группа не найдена", content), status=404)

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{group.name}</h5>
            <p class="card-text"><strong>ID:</strong> {group.id}</p>
            <p class="card-text"><strong>Маршрут:</strong> {group.route}</p>
            <p class="card-text">
                <strong>Вместимость:</strong> {group.max_capacity} мест
            </p>
            <a href="/groups/" class="btn btn-outline-secondary">
                ← К списку групп
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(group.name, content))
