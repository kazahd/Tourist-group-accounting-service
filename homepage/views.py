from django.shortcuts import render


def index(request):
    """Главная страница."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Обработчик ошибки 404 (возвращает шаблон)."""
    # По ТЗ 404 тоже должна быть шаблонной.
    return render(request, "404.html", status=404)
