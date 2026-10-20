-- =============================================
-- Туристический сервис: структура базы данных
-- =============================================

CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    route TEXT NOT NULL,
    max_capacity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    trip_date TEXT NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);