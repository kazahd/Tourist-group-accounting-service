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

* Группа имеет название, маршрут, максимальную вместимость и необязательную фотографию.
* Участник характеризуется именем и возрастом.
* Поездка привязана к определенной группе и имеет дату.
* Взаимодействие: поездка (Trip) связана с группой (Group), участник
  (Participant) может быть привязан к группе (в том числе не привязан ни к какой).

## Модели Django (ПР9)

Слой доступа к данным переведён с ручных SQL-запросов и `sqlite3` на Django ORM.
Модели описаны в `tour_groups/models.py`.

### Group — туристическая группа

* **Поля:** `id`, `name` (CharField, 100), `route` (CharField, 200),
  `max_capacity` (PositiveIntegerField), `slug` (уникальный SlugField).
* **Связи:** `participants` (обратная от `Participant`), `trips` (обратная от `Trip`).
* **Методы:** `has_free_places()`, `__str__()`.
* **Таблица:** `groups` (`Meta.db_table`).

### Participant — участник

* **Поля:** `id`, `name` (CharField, 100), `age` (PositiveIntegerField),
  `is_adult` (вычисляемый GeneratedField), `group` (ForeignKey → Group).
* **Параметры связи:** `on_delete=SET_NULL`, `null=True`, `blank=True`,
  `related_name="participants"` — участник не удаляется вместе с группой.
* **Методы:** `__str__()`.
* **Таблица:** `participants`.

### Trip — поездка

* **Поля:** `id`, `group` (ForeignKey → Group), `trip_date` (DateField),
  `status` (TextChoices: запланирована, отменена, завершена).
* **QuerySet:** `active()`, `cancelled()`, `completed()`, `for_date(date)`.
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

Миграции `tour_groups/migrations/0001_initial.py`–`0005_*.py` хранятся в Git.
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
| 2 | `get_object_or_404(Group, slug=...)` | Получение одного объекта | `group_detail` |
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

Дополнительно статистическая страница формирует проекцию через `values()` и
получает названия пустых групп через `values_list()`. В списках используются
срезы QuerySet через `Paginator`, сортировка `order_by()` и сохранение всех
GET-параметров при переходе между страницами.

Быстрые примеры ORM в `python manage.py shell`:

```python
from datetime import date
from django.db.models import Count
from tour_groups.models import Group, Participant, Trip

group = Group.objects.create(name="Тестовый маршрут", route="Карелия", max_capacity=8)
participant = Participant(name="Анна", age=25, group=group)
participant.save()
Trip.objects.create(group=group, trip_date=date(2027, 8, 1))
Group.objects.filter(name__icontains="тест").order_by("name")
Group.objects.filter(participants__isnull=True).values_list("name", flat=True)
Group.objects.annotate(participant_count=Count("participants")).values(
    "name", "participant_count"
)
Trip.objects.filter(group__name__icontains="Карелия").select_related("group")[:10]
Group.objects.get(pk=group.pk)  # .get() raises DoesNotExist if missing
participant.delete()
group.delete()  # participants become unassigned; trips are cascaded
```

CRUD доступен также через веб-интерфейс: формы поездки создают и изменяют
объекты; участника можно добавить или удалить из карточки группы. Удаление
участника и отмена поездки защищены POST и CSRF.

## Веб-интерфейс (Django)

### Страницы и URL

* `/` — главная страница (`homepage.views.index`);
* `/groups/` — список групп с поиском, фильтром, сортировкой и пагинацией
  (`tour_groups.views.groups`);
* `/groups/stats/` — статистика по группам и участникам
  (`tour_groups.views.group_stats`);
* `/groups/<str:slug>/` — карточка группы с участниками и поездками
  (`tour_groups.views.group_detail`);
* `/trips/` — список поездок с Django GET-формой фильтра, сортировкой и пагинацией
  (`tour_trips.views.trips`);
* `/trips/create/` — создание поездки через ModelForm;
* `/trips/<int:trip_id>/edit/` — изменение поездки через ModelForm;
* `/trips/<int:trip_id>/` — карточка поездки (`tour_trips.views.trip_detail`).

Настроена кастомная обработка ошибки 404 (`homepage.views.page_not_found`),
шаблон — `templates/404.html`.

## Практическая работа 10: Django ORM и Admin

Индивидуальный сквозной проект выполнен на предметной области учета
туристических групп: `Group` соответствует основному объекту учета,
`Participant` — пользователю сервиса, `Trip` — бронируемому событию.
Требования задания перенесены на эти сущности, без замены темы проекта.

### Административная панель

Создайте администратора командой `python manage.py createsuperuser` и откройте
`/admin/`. Все три модели зарегистрированы. Для списков настроены колонки,
поиск, фильтры, сортировка и размер страницы. На странице группы доступно
inline-редактирование участников и поездок; отдельные списки позволяют
управлять ими независимо.

### Дополнительные возможности ORM

* `Trip.Status` — `TextChoices` со статусами запланированной, отмененной и
  завершенной поездки.
* `TripQuerySet` предоставляет `active()`, `cancelled()`, `completed()` и
  `for_date(date)`; фильтр статуса в расписании использует этот API.
* `Group.slug` формируется из названия, уникален и применяется в URL через
  `get_absolute_url()`; неизвестный slug возвращает 404.
* `Participant.is_adult` — вычисляемое поле БД `GeneratedField`, зависящее
  от возраста. Его нельзя редактировать вручную.
* Поездки фильтруются по названию группы, диапазону дат и статусу; сортировка
  идет по белому списку, вывод постраничный. ORM использует `select_related`,
  `annotate`, `Count`, `F`, `aggregate`, `Q`, `exclude` и `get_object_or_404`.
* Django Debug Toolbar подключается в режиме разработки, если установлен
  пакет из `requirements.txt`; откройте `/__debug__/` и панель на странице,
  чтобы посмотреть SQL и число запросов.

### Проверка и демонстрация

```bash
python manage.py makemigrations --check
python manage.py migrate
python manage.py check
python manage.py shell
```

Примеры Django Shell:

```python
from datetime import date
from django.db.models import Count, Q
from tour_groups.models import Group, Participant, Trip

Group.objects.all()
Group.objects.filter(Q(name__icontains="Алтай") | Q(route__icontains="Алтай"))
Group.objects.annotate(participants_count=Count("participants")).values(
    "name", "participants_count"
)
Trip.objects.active().select_related("group")
Trip.objects.for_date(date.today())
Trip.objects.filter(group__name__icontains="поход").order_by("-trip_date")
Participant.objects.filter(is_adult=True).values("name", "age", "is_adult")
group = Group.objects.first()
group.get_absolute_url()
```

Миграции `0002`–`0005` заполняют slug существующим группам, добавляют статусы,
вычисляемый признак совершеннолетия, фотографии и проверку вместимости.
Фикстуры групп и экспорт данных также сохраняют slug.

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
├── tour_groups/                # Django-приложение: группы, модели и формы
│   ├── models.py               # Group, Participant, Trip
│   ├── forms.py                # GET / ModelForm / проверка пользовательского ввода
│   ├── views.py                # списки, карточки, создание и запись участника
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

## Практическая работа 11: Django Forms

Веб-интерфейс использует формы Django для фильтрации, создания и изменения
записей. В предметной области сервиса `Trip` моделирует запись на поездку,
`Participant` — участника группы.

* `TripFilterForm` обрабатывает GET-параметры расписания, проверяет диапазон
  дат через `is_valid()` и передает в ORM только `cleaned_data`.
* `TripForm` — `ModelForm` для создания и изменения поездок. В `clean_trip_date()`
  запрещает дату в прошлом для незавершенной поездки; `clean()` запрещает
  повторную активную поездку той же группы в тот же день. При редактировании
  текущая запись исключается из проверки.
* Форма группы валидирует положительную вместимость и принимает фото. Форма
  записи участника запрещает превышать вместимость группы.
* POST-формы содержат `{% csrf_token %}`. Отмена поездки доступна только через
  POST и метод `Trip.cancel()`; завершенную поездку отменить нельзя.
* Фотография группы — `ImageField(upload_to="groups/")`. В `settings.py`
  заданы `MEDIA_ROOT` и `MEDIA_URL`, в разработке медиа-файлы доступны через
  URL-маршруты. Формы загрузки используют `request.FILES` и
  `enctype="multipart/form-data"`; изображение показано в списке и карточке
  группы и доступно из Django Admin.
* Шаблоны форм показывают `form.non_field_errors`, `field.errors` и
  `field.help_text`; поля стилизованы Bootstrap.

Добавление поездки: `/trips/create/`; редактирование и отмена доступны из
карточки поездки. Создание группы: `/groups/create/`; запись участника — из
карточки группы. Перед запуском выполните `pip install -r requirements.txt`
для установки Django, Pillow и остальных зависимостей, затем примените
миграции командой `python manage.py migrate`.
