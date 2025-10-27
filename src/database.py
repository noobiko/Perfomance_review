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
        
        # Таблица пользователей с ролями
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',  -- 'admin' или 'user'
                employee_id INTEGER,  -- Ссылка на сотрудника
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
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
                created_by INTEGER,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Добавляем тестовых пользователей и сотрудников, если таблицы пусты
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            self.add_sample_users(cursor)
        
        cursor.execute("SELECT COUNT(*) FROM employees")
        if cursor.fetchone()[0] == 0:
            self.add_sample_employees(cursor)
        
        conn.commit()
        conn.close()
    
    def add_sample_users(self, cursor):
        """Добавление тестовых пользователей"""
        # Сначала создаем сотрудников, чтобы получить их ID
        sample_employees = [
            ("admin@company.com", "Админ", "Админов", "Системный администратор", "IT", "2020-01-01", 1),
            ("user@company.com", "Иван", "Иванов", "Разработчик", "IT", "2023-01-15", 1),
            ("petrov@company.com", "Петр", "Петров", "Менеджер", "Продажи", "2022-03-20", 1),
            ("sidorova@company.com", "Мария", "Сидорова", "Аналитик", "Аналитика", "2023-06-10", 1),
        ]
        
        employee_ids = []
        for emp in sample_employees:
            cursor.execute('''
                INSERT INTO employees 
                (email, first_name, last_name, position, department, hire_date, manager_id, created_by, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (*emp, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            employee_ids.append(cursor.lastrowid)
        
        # Теперь создаем пользователей, связывая их с сотрудниками
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password_hash, role, employee_id) VALUES (?, ?, ?, ?)",
            ("admin", admin_hash, "admin", employee_ids[0])  # Связываем с первым сотрудником (Админом)
        )
        
        user_hash = hashlib.sha256("user123".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password_hash, role, employee_id) VALUES (?, ?, ?, ?)",
            ("user", user_hash, "user", employee_ids[1])  # Связываем со вторым сотрудником (Ивановым)
        )
    
    
    def create_user(self, username, password_hash, role="user"):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            conn.commit()
            return True, "Пользователь успешно создан"
        except sqlite3.IntegrityError:
            return False, "Пользователь с таким именем уже существует"
        finally:
            conn.close()
    
    def get_user(self, username):
        """Получение пользователя по имени с включением роли и информации о сотруднике"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.id, u.username, u.password_hash, u.role, u.employee_id, u.created_at,
                e.first_name, e.last_name, e.position, e.department
            FROM users u
            LEFT JOIN employees e ON u.employee_id = e.id
            WHERE u.username = ?
        ''', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_data = {
                'id': user[0],
                'username': user[1],
                'password_hash': user[2],
                'role': user[3],
                'employee_id': user[4],
                'created_at': user[5]
            }
            
            # Добавляем информацию о сотруднике, если есть связь
            if user[6]:  # first_name
                user_data['employee_info'] = {
                    'first_name': user[6],
                    'last_name': user[7],
                    'position': user[8],
                    'department': user[9],
                    'full_name': f"{user[6]} {user[7]}"
                }
            
            return user_data
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
    
    def get_employee_by_id(self, employee_id):
        """Получение сотрудника по ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, first_name, last_name, position, department, email, hire_date
            FROM employees 
            WHERE id = ?
        ''', (employee_id,))
        emp = cursor.fetchone()
        conn.close()
        
        if emp:
            return {
                'id': emp[0],
                'first_name': emp[1],
                'last_name': emp[2],
                'position': emp[3],
                'department': emp[4],
                'email': emp[5],
                'hire_date': emp[6]
            }
        return None
    
    def create_goal(self, employee_id, title, description, expected_result, deadline, task_link, status, progress, created_by=None):
        """Создание новой цели"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO goals 
                (employee_id, title, description, expected_result, deadline, task_link, status, progress, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (employee_id, title, description, expected_result, deadline, task_link, status, progress, created_by))
            conn.commit()
            return True, "Цель успешно создана"
        except Exception as e:
            return False, f"Ошибка при создании цели: {str(e)}"
        finally:
            conn.close()
    
    def get_all_goals(self, user_id=None, user_role=None):
        """Получение всех целей с информацией о сотрудниках"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if user_role == 'admin':
            # Администратор видит все цели
            cursor.execute('''
                SELECT g.id, g.employee_id, e.first_name, e.last_name, g.title, 
                       g.deadline, g.status, g.progress, g.description, g.expected_result, g.task_link, g.created_by
                FROM goals g
                JOIN employees e ON g.employee_id = e.id
                ORDER BY g.deadline, e.last_name
            ''')
        else:
            # Обычный пользователь видит только свои цели
            cursor.execute('''
                SELECT g.id, g.employee_id, e.first_name, e.last_name, g.title, 
                       g.deadline, g.status, g.progress, g.description, g.expected_result, g.task_link, g.created_by
                FROM goals g
                JOIN employees e ON g.employee_id = e.id
                WHERE g.created_by = ?
                ORDER BY g.deadline, e.last_name
            ''', (user_id,))
            
        goals = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': goal[0],
                'employee_id': goal[1],
                'employee_name': f"{goal[2]} {goal[3]}",
                'title': goal[4],
                'deadline': goal[5],
                'status': goal[6],
                'progress': goal[7],
                'description': goal[8],
                'expected_result': goal[9],
                'task_link': goal[10],
                'created_by': goal[11]
            }
            for goal in goals
        ]
    
    def update_goal(self, goal_id, title, description, expected_result, deadline, task_link, status, progress, user_id=None, user_role=None):
        """Обновление цели с проверкой прав"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Проверяем права на редактирование
        if user_role != 'admin':
            cursor.execute("SELECT created_by FROM goals WHERE id = ?", (goal_id,))
            result = cursor.fetchone()
            if not result or result[0] != user_id:
                conn.close()
                return False, "Нет прав для редактирования этой цели"
        
        try:
            cursor.execute('''
                UPDATE goals 
                SET title = ?, description = ?, expected_result = ?, deadline = ?, 
                    task_link = ?, status = ?, progress = ?
                WHERE id = ?
            ''', (title, description, expected_result, deadline, task_link, status, progress, goal_id))
            conn.commit()
            return True, "Цель успешно обновлена"
        except Exception as e:
            return False, f"Ошибка при обновлении цели: {str(e)}"
        finally:
            conn.close()
    
    def delete_goal(self, goal_id, user_id=None, user_role=None):
        """Удаление цели с проверкой прав"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Проверяем права на удаление
        if user_role != 'admin':
            cursor.execute("SELECT created_by FROM goals WHERE id = ?", (goal_id,))
            result = cursor.fetchone()
            if not result or result[0] != user_id:
                conn.close()
                return False, "Нет прав для удаления этой цели"
        
        try:
            cursor.execute('DELETE FROM goals WHERE id = ?', (goal_id,))
            conn.commit()
            return True, "Цель успешно удалена"
        except Exception as e:
            return False, f"Ошибка при удалении цели: {str(e)}"
        finally:
            conn.close()

    def get_employee_by_user_id(self, user_id):
        """Получение сотрудника по ID пользователя"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.id, e.first_name, e.last_name, e.position, e.department, e.email, e.hire_date
            FROM employees e
            JOIN users u ON u.employee_id = e.id
            WHERE u.id = ?
        ''', (user_id,))
        emp = cursor.fetchone()
        conn.close()
        
        if emp:
            return {
                'id': emp[0],
                'first_name': emp[1],
                'last_name': emp[2],
                'position': emp[3],
                'department': emp[4],
                'email': emp[5],
                'hire_date': emp[6]
            }
        return None

    def get_user_by_employee_id(self, employee_id):
        """Получение пользователя по ID сотрудника"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, role, employee_id
            FROM users
            WHERE employee_id = ?
        ''', (employee_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'role': user[2],
                'employee_id': user[3]
            }
        return None

    def link_user_to_employee(self, user_id, employee_id):
        """Связывание пользователя с сотрудником"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET employee_id = ? WHERE id = ?",
                (employee_id, user_id)
            )
            conn.commit()
            return True, "Пользователь успешно связан с сотрудником"
        except Exception as e:
            return False, f"Ошибка при связывании: {str(e)}"
        finally:
            conn.close()

    def get_all_users(self):
        """Получение всех пользователей"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY username")
        users = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': user[0],
                'username': user[1],
                'role': user[2],
                'created_at': user[3]
            }
            for user in users
        ]

    def get_user_by_id(self, user_id):
        """Получение пользователя по ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'role': user[2]
            }
        return None

    def create_employee(self, email, first_name, last_name, position, department, hire_date, manager_id, created_by=None):
        """Создание нового сотрудника"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO employees 
                (email, first_name, last_name, position, department, hire_date, manager_id, created_by, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (email, first_name, last_name, position, department, hire_date, manager_id, created_by, 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            return True, "Сотрудник успешно добавлен"
        except sqlite3.IntegrityError:
            return False, "Сотрудник с таким email уже существует"
        except Exception as e:
            return False, f"Ошибка при добавлении сотрудника: {str(e)}"
        finally:
            conn.close()

    def get_users_without_employee(self):
        """Получение пользователей без связи с сотрудниками"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, role 
            FROM users 
            WHERE employee_id IS NULL
        ''')
        users = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': user[0],
                'username': user[1],
                'role': user[2]
            }
            for user in users
        ]

    def get_employees_without_user(self):
        """Получение сотрудников без связи с пользователями"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.id, e.first_name, e.last_name, e.position, e.department
            FROM employees e
            LEFT JOIN users u ON e.id = u.employee_id
            WHERE u.id IS NULL
        ''')
        employees = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': emp[0],
                'first_name': emp[1],
                'last_name': emp[2],
                'position': emp[3],
                'department': emp[4]
            }
            for emp in employees
        ]
    
    def create_employee_with_user(self, email, first_name, last_name, position, department, hire_date, manager_id, username, password, role="user", created_by=None):
        """Создание сотрудника и связанного пользователя"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Создаем сотрудника
            cursor.execute('''
                INSERT INTO employees 
                (email, first_name, last_name, position, department, hire_date, manager_id, created_by, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (email, first_name, last_name, position, department, hire_date, manager_id, created_by, 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            employee_id = cursor.lastrowid
            
            # Создаем пользователя
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role, employee_id) VALUES (?, ?, ?, ?)",
                (username, password_hash, role, employee_id)
            )
            
            conn.commit()
            return True, "Сотрудник и пользователь успешно созданы"
            
        except Exception as e:
            conn.rollback()
            return False, f"Ошибка при создании: {str(e)}"
        finally:
            conn.close()