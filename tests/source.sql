CREATE TABLE table_one (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO table_one (id, name, age, created_at) VALUES
    (1, 'Alice', 30, '2023-01-01 10:00:00'),
    (2, 'Bob', 25, '2023-01-02 11:00:00'),
    (3, 'Charlie', 35, '2023-01-03 12:00:00'),
    (4, 'David', 28, '2023-01-04 13:00:00'),
    (5, 'Eve', 22, '2023-01-05 14:00:00'),
    (6, 'Frank', 40, '2023-01-06 15:00:00'),
    (7, 'Grace', 27, '2023-01-07 16:00:00'),
    (8, 'Hank', 33, '2023-01-08 17:00:00'),
    (9, 'Ivy', 29, '2023-01-09 18:00:00'),
    (10, 'Jack', 31, '2023-01-10 19:00:00');
);