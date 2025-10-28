# main_interface_admin.py
import customtkinter as ctk
from tkinter import messagebox
from tkinter import Text
import sqlite3
from tkinter import ttk
from datetime import datetime

class AdminInterface:
    def __init__(self, root, db_manager, current_user):
        self.root = root
        self.db = db_manager
        self.current_user = current_user
        self.selected_goal_id = None

        self.create_interface()
        self.load_employees()
        self.load_goals()
        self.load_users()
    
    def create_interface(self):
        """Создание интерфейса администратора"""
        self.create_menu()
        
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.goals_frame = self.notebook.add("Просмотр целей")
        self.employees_frame = self.notebook.add("Сотрудники")
        self.users_frame = self.notebook.add("Пользователи")
        
        self.setup_goals_tab()
        self.setup_employees_tab()
        self.setup_users_tab()
    
    def create_menu(self):
        """Создание меню администратора"""
        menubar = ctk.CTkFrame(self.root, height=30)
        menubar.pack(fill='x', padx=10, pady=5)
        
        user_menu = ctk.CTkButton(menubar, text=f"Администратор: {self.current_user['username']}", 
                                 command=self.logout, width=250)
        user_menu.pack(side='left', padx=5)
        
        role_label = ctk.CTkLabel(menubar, text="Роль: Администратор", 
                                 text_color="red", font=("Arial", 12, "bold"))
        role_label.pack(side='left', padx=10)

    def setup_goals_tab(self):
        """Настройка вкладки просмотра целей (только просмотр для администратора)"""
        # Заголовок с пояснением
        info_label = ctk.CTkLabel(self.goals_frame, 
                                 text="Режим просмотра: администратор может только просматрить и удалять цели", 
                                 text_color="blue", font=("Arial", 12))
        info_label.pack(pady=5)
        
        # Таблица целей
        tree_frame = ctk.CTkFrame(self.goals_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("ID", "Сотрудник", "Название", "Срок", "Статус", "Прогресс", "Создал")
        self.goals_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Настройка колонок
        self.goals_tree.heading("ID", text="ID")
        self.goals_tree.heading("Сотрудник", text="Сотрудник")
        self.goals_tree.heading("Название", text="Название")
        self.goals_tree.heading("Срок", text="Срок")
        self.goals_tree.heading("Статус", text="Статус")
        self.goals_tree.heading("Прогресс", text="Прогресс")
        self.goals_tree.heading("Создал", text="Создал")
        
        self.goals_tree.column("ID", width=50)
        self.goals_tree.column("Сотрудник", width=150)
        self.goals_tree.column("Название", width=200)
        self.goals_tree.column("Срок", width=100)
        self.goals_tree.column("Статус", width=100)
        self.goals_tree.column("Прогресс", width=80)
        self.goals_tree.column("Создал", width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.goals_tree.yview)
        self.goals_tree.configure(yscrollcommand=scrollbar.set)
        
        self.goals_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопки управления
        button_frame = ctk.CTkFrame(self.goals_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkButton(button_frame, text="Обновить список", command=self.load_goals).pack(side='left', padx=5)
        ctk.CTkButton(button_frame, text="Удалить выбранную цель", 
                     command=self.delete_goal, fg_color="red", hover_color="darkred").pack(side='left', padx=5)
        
        # Привязка событий
        self.goals_tree.bind('<ButtonRelease-1>', self.on_goal_select)

    def setup_employees_tab(self):
        """Настройка вкладки управления сотрудниками"""
        ctk.CTkLabel(self.employees_frame, text="Управление сотрудниками", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Форма добавления сотрудника
        form_frame = ctk.CTkFrame(self.employees_frame)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Добавить нового сотрудника", 
                    font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Поля формы
        fields = [
            ("Имя:", "first_name"),
            ("Фамилия:", "last_name"),
            ("Email:", "email"),
            ("Должность:", "position"),
            ("Отдел:", "department"),
            ("Дата приема (ГГГГ-ММ-ДД):", "hire_date"),
            ("ID менеджера:", "manager_id")
        ]
        
        self.employee_entries = {}
        for i, (label, field) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label).grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
            entry = ctk.CTkEntry(form_frame, width=300)
            entry.grid(row=i+1, column=1, padx=5, pady=5, sticky="we")
            self.employee_entries[field] = entry
        
        # Кнопка добавления
        ctk.CTkButton(form_frame, text="Добавить сотрудника", 
                     command=self.add_employee).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        
        # Таблица сотрудников
        tree_frame = ctk.CTkFrame(self.employees_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("ID", "Имя", "Фамилия", "Email", "Должность", "Отдел", "Дата приема")
        self.employees_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.employees_tree.heading(col, text=col)
            self.employees_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.employees_tree.yview)
        self.employees_tree.configure(yscrollcommand=scrollbar.set)
        
        self.employees_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопка обновления
        ctk.CTkButton(self.employees_frame, text="Обновить список сотрудников", 
                     command=self.load_employees).pack(pady=5)

    def setup_users_tab(self):
        """Настройка вкладки управления пользователями"""
        ctk.CTkLabel(self.users_frame, text="Управление пользователями", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Форма добавления пользователя
        form_frame = ctk.CTkFrame(self.users_frame)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Добавить нового пользователя", 
                    font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Поля формы
        ctk.CTkLabel(form_frame, text="Имя пользователя:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.new_username = ctk.CTkEntry(form_frame, width=200)
        self.new_username.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(form_frame, text="Пароль:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.new_password = ctk.CTkEntry(form_frame, width=200, show="*")
        self.new_password.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(form_frame, text="Роль:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.new_role = ctk.CTkComboBox(form_frame, values=["user", "admin"], width=200, state="readonly")
        self.new_role.set("user")
        self.new_role.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        # Кнопка добавления
        ctk.CTkButton(form_frame, text="Добавить пользователя", 
                     command=self.add_user).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Таблица пользователей
        tree_frame = ctk.CTkFrame(self.users_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("ID", "Имя пользователя", "Роль", "Дата создания")
        self.users_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопка обновления
        ctk.CTkButton(self.users_frame, text="Обновить список пользователей", 
                     command=self.load_users).pack(pady=5)

    def load_employees(self):
        """Загрузка списка сотрудников"""
        try:
            # Очищаем таблицу
            for item in self.employees_tree.get_children():
                self.employees_tree.delete(item)
            
            employees = self.db.get_all_employees()
            for emp in employees:
                self.employees_tree.insert("", "end", values=(
                    emp['id'],
                    emp['first_name'],
                    emp['last_name'],
                    emp.get('email', ''),
                    emp['position'],
                    emp['department'],
                    emp.get('hire_date', '')
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить сотрудников: {str(e)}")

    def load_goals(self):
        """Загрузка целей в таблицу"""
        try:
            # Очищаем таблицу
            for item in self.goals_tree.get_children():
                self.goals_tree.delete(item)
            
            # Получаем цели из базы данных (админ видит все цели)
            goals = self.db.get_all_goals(user_id=self.current_user['id'], user_role='admin')
            
            # Заполняем таблицу
            for goal in goals:
                # Получаем имя создателя цели
                creator_name = "Неизвестно"
                if goal['created_by']:
                    creator = self.db.get_user_by_id(goal['created_by'])
                    if creator:
                        creator_name = creator['username']
                
                self.goals_tree.insert("", "end", values=(
                    goal['id'],
                    goal['employee_name'],
                    goal['title'],
                    goal['deadline'],
                    goal['status'],
                    f"{goal['progress']}%",
                    creator_name
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить цели: {str(e)}")

    def load_users(self):
        """Загрузка списка пользователей"""
        try:
            # Очищаем таблицу
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            users = self.db.get_all_users()
            for user in users:
                self.users_tree.insert("", "end", values=(
                    user['id'],
                    user['username'],
                    user['role'],
                    user['created_at']
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей: {str(e)}")

    def add_employee(self):
        """Добавление нового сотрудника"""
        try:
            # Получаем данные из формы
            first_name = self.employee_entries['first_name'].get().strip()
            last_name = self.employee_entries['last_name'].get().strip()
            email = self.employee_entries['email'].get().strip()
            position = self.employee_entries['position'].get().strip()
            department = self.employee_entries['department'].get().strip()
            hire_date = self.employee_entries['hire_date'].get().strip()
            manager_id = self.employee_entries['manager_id'].get().strip()
            
            # Валидация
            if not all([first_name, last_name, email, position, department, hire_date]):
                messagebox.showwarning("Предупреждение", "Заполните все обязательные поля")
                return
            
            # Преобразуем manager_id в int, если указан
            try:
                manager_id = int(manager_id) if manager_id else 1
            except ValueError:
                messagebox.showwarning("Предупреждение", "ID менеджера должен быть числом")
                return
            
            # Добавляем сотрудника в базу
            success, message = self.db.create_employee(
                email=email,
                first_name=first_name,
                last_name=last_name,
                position=position,
                department=department,
                hire_date=hire_date,
                manager_id=manager_id,
                created_by=self.current_user['id']
            )
            
            if success:
                messagebox.showinfo("Успех", message)
                self.clear_employee_form()
                self.load_employees()
            else:
                messagebox.showerror("Ошибка", message)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении сотрудника: {str(e)}")

    def add_user(self):
        """Добавление нового пользователя"""
        username = self.new_username.get().strip()
        password = self.new_password.get()
        role = self.new_role.get()
        
        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля")
            return
        
        if len(password) < 4:
            messagebox.showwarning("Предупреждение", "Пароль должен содержать минимум 4 символа")
            return
        
        success, message = self.db.create_user(username, password, role)
        
        if success:
            messagebox.showinfo("Успех", message)
            self.new_username.delete(0, 'end')
            self.new_password.delete(0, 'end')
            self.new_role.set("user")
            self.load_users()
        else:
            messagebox.showerror("Ошибка", message)

    def delete_goal(self):
        """Удаление выбранной цели"""
        selected = self.goals_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите цель для удаления")
            return
        
        goal_id = self.goals_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту цель?"):
            success, message = self.db.delete_goal(goal_id, self.current_user['id'], 'admin')
            
            if success:
                messagebox.showinfo("Успех", message)
                self.load_goals()
            else:
                messagebox.showerror("Ошибка", message)

    def on_goal_select(self, event):
        """Обработка выбора цели в таблице"""
        selected = self.goals_tree.selection()
        if selected:
            self.selected_goal_id = self.goals_tree.item(selected[0])['values'][0]

    def clear_employee_form(self):
        """Очистка формы сотрудника"""
        for entry in self.employee_entries.values():
            entry.delete(0, 'end')


    def setup_users_tab(self):
        """Настройка вкладки управления пользователями"""
        # ... существующий код ...
        
        # Добавляем функционал связывания с сотрудниками
        link_frame = ctk.CTkFrame(self.users_frame)
        link_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(link_frame, text="Связывание пользователя с сотрудником", 
                    font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        
        ctk.CTkLabel(link_frame, text="Пользователь:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.link_user_combo = ctk.CTkComboBox(link_frame, width=200, state="readonly")
        self.link_user_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(link_frame, text="Сотрудник:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.link_employee_combo = ctk.CTkComboBox(link_frame, width=200, state="readonly")
        self.link_employee_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkButton(link_frame, text="Связать", 
                    command=self.link_user_employee).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Обновляем комбобоксы при загрузке
        self.update_link_comboboxes()

    def update_link_comboboxes(self):
        """Обновление комбобоксов для связывания"""
        # Пользователи без связей
        users = self.db.get_users_without_employee()
        user_options = [f"{user['username']} (ID: {user['id']})" for user in users]
        self.link_user_combo.configure(values=user_options)
        
        # Сотрудники без пользователей
        employees = self.db.get_employees_without_user()
        employee_options = [f"{emp['first_name']} {emp['last_name']} (ID: {emp['id']})" for emp in employees]
        self.link_employee_combo.configure(values=employee_options)

    def link_user_employee(self):
        """Связывание пользователя с сотрудником"""
        user_display = self.link_user_combo.get()
        employee_display = self.link_employee_combo.get()
        
        if not user_display or not employee_display:
            messagebox.showwarning("Предупреждение", "Выберите пользователя и сотрудника")
            return
        
        # Извлекаем ID из строк вида "username (ID: 1)"
        user_id = int(user_display.split("ID: ")[1].rstrip(")"))
        employee_id = int(employee_display.split("ID: ")[1].rstrip(")"))
        
        success, message = self.db.link_user_to_employee(user_id, employee_id)
        
        if success:
            messagebox.showinfo("Успех", message)
            self.update_link_comboboxes()
            self.load_users()
        else:
            messagebox.showerror("Ошибка", message)

    def logout(self):
        """Выход из системы"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выйти?"):
            self.root.destroy()