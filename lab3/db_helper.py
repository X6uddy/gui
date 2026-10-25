import sqlite3
from contextlib import closing
from pathlib import Path


# путь строится от расположения файла, поэтому не зависит от папки запуска
DB_PATH = Path(__file__).parent / "test_db_lab3.db"

SCHEMA = '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT DEFAULT 'user'
    );

    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER DEFAULT 0
    );

    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    );
'''

# таблица -> (SQL вставки, строки данных)
TEST_DATA = {
    "users": (
        "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
        [
            ('Иван Иванов', 'ivan@example.com', 'admin'),
            ('Анна Смирнова', 'anna@example.com', 'user'),
            ('Петр Петров', 'petr@example.com', 'user'),
            ('Елена Сидорова', 'elena@example.com', 'manager'),
        ],
    ),
    "products": (
        "INSERT INTO products (title, price, stock) VALUES (?, ?, ?)",
        [
            ('Ноутбук', 75000.00, 10),
            ('Смартфон', 45000.50, 25),
            ('Беспроводные наушники', 8900.00, 50),
            ('Клавиатура', 3500.00, 15),
        ],
    ),
    "orders": (
        "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",
        [
            (1, 1, 1),
            (2, 2, 2),
            (3, 3, 1),
            (2, 4, 1),
        ],
    ),
}


class Dbhelper:

    @staticmethod
    def create_test_db(db_path: Path = DB_PATH):
        """Пересоздаёт тестовую SQLite БД: схема + тестовые данные"""

        db_path = Path(db_path)
        if db_path.exists():
            db_path.unlink()
            print(f"Старый файл {db_path} удален.")

        # sqlite3.connect как менеджер контекста только фиксирует транзакцию, но не закрывает
        # соединение, поэтому используем closing
        with closing(sqlite3.connect(db_path)) as conn, conn:
            conn.executescript(SCHEMA)
            for insert_sql, rows in TEST_DATA.values():
                conn.executemany(insert_sql, rows)

        print(f"База данных '{db_path}' успешно создана и заполнена тестовыми данными!")
