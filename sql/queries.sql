-- 1. Выборка: Список всех групп
SELECT id, name, route, max_capacity FROM groups ORDER BY name;

-- 2. Выборка: Список участников (с именем группы через JOIN)
SELECT p.id, p.name, p.age, g.name AS group_name 
FROM participants p 
LEFT JOIN groups g ON p.group_id = g.id 
ORDER BY p.name;

-- 3. Фильтрация (WHERE): Группы с вместимостью >= 10
SELECT id, name, max_capacity FROM groups WHERE max_capacity >= 10 ORDER BY max_capacity;

-- 4. Фильтрация (WHERE): Участники старше 18 лет
SELECT id, name, age FROM participants WHERE age >= 18 ORDER BY age;

-- 5. JOIN: Поездки с названиями групп
SELECT t.id, t.trip_date, g.name AS group_name 
FROM trips t 
JOIN groups g ON t.group_id = g.id 
ORDER BY t.trip_date;

-- 6. JOIN: Участники без группы
SELECT p.id, p.name FROM participants p 
LEFT JOIN groups g ON p.group_id = g.id 
WHERE p.group_id IS NULL;

-- 7. Агрегация (COUNT): Общее количество групп
SELECT COUNT(*) AS total_groups FROM groups;

-- 8. Агрегация (COUNT): Количество участников в каждой группе (GROUP BY)
SELECT g.name AS group_name, COUNT(p.id) AS participants_count 
FROM groups g 
LEFT JOIN participants p ON g.id = p.group_id 
GROUP BY g.id, g.name;

-- 9. Группировка (HAVING): Группы, где больше 1 участника
SELECT g.name AS group_name, COUNT(p.id) AS participants_count 
FROM groups g 
JOIN participants p ON g.id = p.group_id 
GROUP BY g.id, g.name 
HAVING COUNT(p.id) > 1;

-- 10. Агрегация: Средний возраст всех участников
SELECT AVG(age) AS average_age FROM participants;
