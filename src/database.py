# database.py
import sqlite3
from datetime import datetime
import hashlib

class DatabaseManager:
    def __init__(self, db_name="goals_system.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица сотрудников 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                position TEXT NOT NULL,
                department TEXT NOT NULL,
                hire_date TEXT NOT NULL,
                manager_id INTEGER NOT NULL,
                created_by INTEGER,
                created_date TEXT NOT NULL,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Таблица целей 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                expected_result TEXT NOT NULL,
                deadline DATE NOT NULL,
                task_link TEXT,
                status TEXT NOT NULL,
                progress INTEGER NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            self.add_sample_users(cursor)

        cursor.execute("SELECT COUNT(*) FROM employees")
        if cursor.fetchone()[0] == 0:
            self.add_sample_employees(cursor)

        conn.commit()
        conn.close()


    

    def create_user(self, username, password_hash):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            return True, "Пользователь успешно создан"
        except sqlite3.IntegrityError:
            return False, "Пользователь с таким именем уже существует"
        finally:
            conn.close()

    def add_sample_employees(self, cursor):
        """Добавление тестовых сотрудников"""
        sample_employees = [
            ("ivanov@company.com", "Иван", "Иванов", "Разработчик", "IT", "2023-01-15", 1),
            ("petrov@company.com", "Петр", "Петров", "Менеджер", "Продажи", "2022-03-20", 1),
            ("sidorova@company.com", "Мария", "Сидорова", "Аналитик", "Аналитика", "2023-06-10", 1),
            ("smirnov@company.com", "Алексей", "Смирнов", "Дизайнер", "Дизайн", "2022-11-05", 1),
        ]
        
        for emp in sample_employees:
            cursor.execute('''
                INSERT INTO employees 
                (email, first_name, last_name, position, department, hire_date, manager_id, created_by, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (*emp, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def add_sample_users(self, cursor):
        """Добавление тестовых пользователей"""
        # Администратор
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("admin", admin_hash, "admin")
        )
        
        # Обычный пользователь
        user_hash = hashlib.sha256("user123".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("user", user_hash, "user")
        )
    
    def get_user(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'password_hash': user[2],
                'role': user[3],
                'created_at': user[4]
            }
        return None
    
    def get_all_employees(self):
        """Получение всех сотрудников"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, first_name, last_name, position, department 
            FROM employees 
            ORDER BY last_name, first_name
        ''')
        employees = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': emp[0],
                'first_name': emp[1],
                'last_name': emp[2],
                'position': emp[3],
                'department': emp[4],
                'display_name': f"{emp[1]} {emp[2]} ({emp[3]})"
            }
            for emp in employees
        ]