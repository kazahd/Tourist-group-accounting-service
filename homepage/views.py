from django.http import HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
)


def page(title, content):
    """Единый HTML-каркас страницы."""
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link href="{BOOTSTRAP_CSS}" rel="stylesheet">
    </head>
    <body class="bg-light">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
            <div class="container">
                <a class="navbar-brand" href="/">Туристический сервис</a>
                <div class="navbar-nav">
                    <a class="nav-link" href="/groups/">Группы</a>
                    <a class="nav-link" href="/trips/">Поездки</a>
                </div>
            </div>
        </nav>
        <div class="container">
            {content}
        </div>
    </body>
    </html>
    """


def index(request):
    content = """
    <h1 class="display-4">Сервис учета туристических групп</h1>
    <p class="lead">Управление группами, участниками и поездками.</p>
    <hr class="my-4">
    <p>Выберите раздел для просмотра:</p>
    <a href="/groups/" class="btn btn-primary me-2">Группы</a>
    <a href="/trips/" class="btn btn-secondary">Поездки</a>
    """
    return HttpResponse(page("Главная", content))


def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
