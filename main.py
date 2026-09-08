from datetime import date

group_name = "Поход в горы"
route = "Алтай"
max_capacity = 10
current_members = 3

new_participant = "Анна Иванова"
participant_age = 28

trip_date = date(2026, 7, 15)

def can_join(current, max_capacity):
    if current < max_capacity:
        return True
    return False

def check_age(age):
    if age >= 18:
        return "Возраст подходит"
    else:
        return "Требуется разрешение родителей"

def get_group_status(current, max_capacity):
    if current < max_capacity:
        free = max_capacity - current
        return f"Свободно {free} мест. Можно присоединиться!"
    else:
        return "Группа заполнена. Мест нет."

print("Туристическая группа")

print(f"Группа: {group_name}")
print(f"Маршрут: {route}")
print(f"Участников: {current_members} из {max_capacity}")
print(f"Дата поездки: {trip_date}")
print(f"Новый участник: {new_participant} ({participant_age} лет)")
print(f"Проверка возраста: {check_age(participant_age)}")

if can_join(current_members, max_capacity):
    print("Результат: Участник может быть добавлен!")
    current_members += 1
else:
    print("Результат: Добавление невозможно - группа переполнена")

print(f"\nОбновленное количество участников: {current_members}")
print(get_group_status(current_members, max_capacity))
