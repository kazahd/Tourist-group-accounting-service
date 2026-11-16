# Сервис учета туристических групп

Приложение для управления туристическими группами, участниками и поездками.
Включает консольную версию и веб-интерфейс на базе фреймворка Django.

## Назначение

Сервис позволяет вести учет туристических групп, добавлять участников,
проверять возрастные ограничения, планировать поездки и просматривать
информацию через веб-браузер.

Приложение позволяет:
* просматривать и добавлять группы;
* просматривать и добавлять участников;
* привязывать участников к группам;
* фильтровать участников по возрасту;
* просматривать и добавлять поездки;
* искать, фильтровать, сортировать и постранично выводить данные
  через веб-интерфейс.

## Используемые технологии

* Python 3;
* Django 5.2 — веб-фреймворк;
* Django ORM — слой доступа к данным (ПР9);
* SQLite — база данных (`db.sqlite3`, создаётся миграциями);
* HTML, CSS и Bootstrap 5.3 — оформление страниц;
* pytest — автоматизированные тесты;
* flake8 — проверка качества кода.

## Целевая аудитория

Организаторы походов, туристические клубы и руководители групп, которым
необходимо вести учет участников и планировать поездки.

## Предметная область

Управление туристическими группами и поездками.

* Группа имеет название, маршрут и максимальную вместимость.
* Участник характеризуется именем и возрастом.
* Поездка привязана к определенной группе и имеет дату.
* Взаимодействие: поездка (Trip) связана с группой (Group), участник
  (Participant) может быть привязан к группе (в том числе не привязан ни к какой).

## Модели Django (ПР9)

Слой доступа к данным переведён с ручных SQL-запросов и `sqlite3` на Django ORM.
Модели описаны в `tour_groups/models.py`.

### Group — туристическая группа

* **Поля:** `id`, `name` (CharField, 100), `route` (CharField, 200),
  `max_capacity` (PositiveIntegerField).
* **Связи:** `participants` (обратная от `Participant`), `trips` (обратная от `Trip`).
* **Методы:** `has_free_places()`, `__str__()`.
* **Таблица:** `groups` (`Meta.db_table`).

### Participant — участник

* **Поля:** `id`, `name` (CharField, 100), `age` (PositiveIntegerField),
  `group` (ForeignKey → Group).
* **Параметры связи:** `on_delete=SET_NULL`, `null=True`, `blank=True`,
  `related_name="participants"` — участник не удаляется вместе с группой.
* **Методы:** `is_adult()`, `__str__()`.
* **Таблица:** `participants`.

### Trip — поездка

* **Поля:** `id`, `group` (ForeignKey → Group), `trip_date` (DateField).
* **Параметры связи:** `on_delete=CASCADE`, `related_name="trips"` —
  поездка удаляется вместе с группой.
* **Методы:** `__str__()`.
* **Таблица:** `trips`.

## Миграции

Структура БД управляется миграциями Django:

```bash
python manage.py makemigrations tour_groups
python manage.py migrate
python manage.py sqlmigrate tour_groups 0001   # посмотреть SQL
```

Файл миграции — `tour_groups/migrations/0001_initial.py` — хранится в Git.
Локальная БД `db.sqlite3` в Git не попадает (см. `.gitignore`).

## Перенос данных из БД ПР7

Данные из старой базы `data/tourist.sqlite` выгружаются в JSON-фикстуры
скриптом `scripts/export_fixtures.py` и загружаются в Django-БД командой
`loaddata`:

```bash
python scripts/export_fixtures.py
python manage.py loaddata fixtures/groups.json
python manage.py loaddata fixtures/participants.json
python manage.py loaddata fixtures/trips.json
```

Порядок загрузки важен: сначала `groups`, затем `participants` и `trips`
(из-за внешних ключей).

## ORM-запросы в проекте

Ниже — сводка ORM-выражений, использованных в представлениях
(`tour_groups/views.py`, `tour_trips/views.py`).

| № | Выражение | Категория | Где |
|---|---|---|---|
| 1 | `Group.objects.all()` | Базовое получение набора | `groups` |
| 2 | `get_object_or_404(Group, pk=...)` | Получение одного объекта | `group_detail` |
| 3 | `filter(max_capacity__gte=...)` | Фильтр по одному условию | `groups` |
| 4 | `filter(trip_date__gte=..., trip_date__lte=...)` | Фильтр по нескольким | `trips` |
| 5 | `filter(group__name__icontains=...)` | Фильтр по связанной модели | `trips` |
| 6 | `exclude(participants_count=0)` | Исключение записей | `group_stats` |
| 7 | `filter(name__icontains=...)` | Поиск по строковому полю | `groups` |
| 8 | `filter(Q(name__icontains=...) \| Q(route__icontains=...))` | Поиск по нескольким полям | `groups` |
| 9 | `order_by("name")` | Сортировка по одному полю | `groups` |
| 10 | `order_by("-participants_count", "name")` / `order_by("group__name")` | Сортировка по нескольким / связанному | `group_stats`, `trips` |
| 11 | `group.participants.all()` | Обращение через `related_name` | `group_detail` |
| 12 | `select_related("group")` | Оптимизация JOIN | `trips`, `trip_detail` |
| 13 | `Participant.objects.aggregate(Avg, Max, Min)` | Сводный показатель | `group_stats` |
| 14 | `annotate(participants_count=Count(...), trips_count=Count(...))` | Показатель по группам | `groups`, `group_stats` |
| 15 | `Paginator(qs, 10).page(number)` | Постраничный вывод | `groups`, `trips` |

## Веб-интерфейс (Django)

### Страницы и URL

* `/` — главная страница (`homepage.views.index`);
* `/groups/` — список групп с поиском, фильтром, сортировкой и пагинацией
  (`tour_groups.views.groups`);
* `/groups/stats/` — статистика по группам и участникам
  (`tour_groups.views.group_stats`);
* `/groups/<int:group_id>/` — карточка группы с участниками и поездками
  (`tour_groups.views.group_detail`);
* `/trips/` — список поездок с фильтром, сортировкой и пагинацией
  (`tour_trips.views.trips`);
* `/trips/<int:trip_id>/` — карточка поездки (`tour_trips.views.trip_detail`).

Настроена кастомная обработка ошибки 404 (`homepage.views.page_not_found`),
шаблон — `templates/404.html`.

### Параметры запроса

Список групп (`/groups/`):

* `?q=текст` — поиск по названию и маршруту;
* `?min_capacity=число` — минимальная вместимость;
* `?sort=name|name_desc|capacity|capacity_desc|participants` — сортировка;
* `?page=N` — номер страницы.

Список поездок (`/trips/`):

* `?group=текст` — фильтр по названию группы;
* `?from=YYYY-MM-DD` и `?to=YYYY-MM-DD` — диапазон дат;
* `?sort=date|date_desc|group` — сортировка;
* `?page=N` — номер страницы.

Все параметры валидируются: недопустимые значения игнорируются или
заменяются значениями по умолчанию, поле сортировки выбирается только
из белого списка.

### Оформление

Используется Bootstrap 5.3 (подключён через CDN). Общий каркас —
`templates/base.html` с навигационным меню (`templates/includes/navigation.html`).

## Структура проекта

```text
tourist_service/
├── README.md
├── requirements.txt
├── manage.py
├── main.py                     # Консольная версия (ПР1–ПР3)
├── storage.py                  # Работа с JSON
├── utils.py                    # Ввод данных
├── .flake8                     # Настройки линтера
├── db.sqlite3                  # Локальная БД (в Git не входит)
├── models/                     # Классы предметной области (ПР3, консольная версия)
│   ├── __init__.py
│   ├── groups.py
│   ├── participants.py
│   ├── trips.py
│   └── relations.py
├── data/                       # Данные ПР7
│   └── tourist.sqlite          # Старая БД (используется только для переноса)
├── scripts/
│   └── export_fixtures.py      # Выгрузка старой БД в JSON-фикстуры
├── fixtures/                   # JSON-фикстуры Django
│   ├── groups.json
│   ├── participants.json
│   └── trips.json
├── tests/                      # Тесты pytest
├── tourist_service/            # Настройки Django-проекта
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── homepage/                   # Django-приложение: главная и 404
│   ├── views.py
│   └── urls.py
├── tour_groups/                # Django-приложение: группы и модели
│   ├── models.py               # Group, Participant, Trip
│   ├── views.py                # groups(), group_stats(), group_detail()
│   ├── urls.py
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── templates/tour_groups/
└── tour_trips/                 # Django-приложение: поездки
    ├── views.py                # trips(), trip_detail()
    ├── urls.py
    └── templates/tour_trips/
```

## Запуск

```bash
python -m venv venv
venv\Scripts\activate           # Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Открыть в браузере: http://127.0.0.1:8000/

Консольный просмотр локальной БД:

```bash
python -m sqlite3 db.sqlite3
```

Старая БД ПР7 (только для переноса данных):

```bash
python -m sqlite3 data/tourist.sqlite
```
```

---
