# main_interface.py
import customtkinter as ctk
from tkinter import messagebox
from tkinter import Text
import sqlite3

class MainInterface:
    def __init__(self, root, db_manager, current_user):
        self.root = root
        self.db = db_manager
        self.current_user = current_user
        
        self.create_interface()
        self.load_employees()
        self.load_goals()
    
    def create_interface(self):
        """Создание основного интерфейса"""
        self.create_menu()
        
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.goals_frame = self.notebook.add("Цели")
        self.valuation_frame = self.notebook.add("Оценки")
        self.recommendations_frame = self.notebook.add("Рекомендации")
        
        self.setup_goals_tab()
        self.setup_valuation_tab()
        self.setup_recommendations_tab()
    
    def create_menu(self):
        """Создание меню"""
        menubar = ctk.CTkFrame(self.root, height=30)
        menubar.pack(fill='x', padx=10, pady=5)
        
        # Получаем информацию о сотруднике
        employee_info = ""
        if self.current_user.get('employee_info'):
            emp = self.current_user['employee_info']
            employee_info = f" - {emp['full_name']} ({emp['position']})"
        
        user_menu = ctk.CTkButton(menubar, 
                                text=f"Пользователь: {self.current_user['username']}{employee_info}", 
                                command=self.logout, width=300)
        user_menu.pack(side='left', padx=5)

    def setup_goals_tab(self):
        """Настройка вкладки целей"""
        add_frame = ctk.CTkFrame(self.goals_frame)
        add_frame.pack(fill='x', padx=10, pady=5)
        
        # Выбор сотрудника
        ctk.CTkLabel(add_frame, text="Сотрудник:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.employee_var = ctk.StringVar()
        self.employee_combo = ctk.CTkComboBox(add_frame, variable=self.employee_var, width=300, state="readonly")
        self.employee_combo.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        
        # Основные поля
        ctk.CTkLabel(add_frame, text="Название цели:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.goal_title = ctk.CTkEntry(add_frame, width=400)
        self.goal_title.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        
        ctk.CTkLabel(add_frame, text="Описание:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.goal_description = Text(add_frame, width=400, height=3, wrap="word")
        self.goal_description.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        
        ctk.CTkLabel(add_frame, text="Ожидаемый результат:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.expected_result = Text(add_frame, width=400, height=3, wrap="word")
        self.expected_result.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        
        # Срок и ссылка
        ctk.CTkLabel(add_frame, text="Срок (ГГГГ-ММ-ДД):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.goal_deadline = ctk.CTkEntry(add_frame, width=150)
        self.goal_deadline.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(add_frame, text="Ссылка на задачу:").grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.task_link = ctk.CTkEntry(add_frame, width=200)
        self.task_link.grid(row=4, column=3, padx=5, pady=5, sticky="we")
        
        # Статус и прогресс
        ctk.CTkLabel(add_frame, text="Статус:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.goal_status = ctk.CTkComboBox(add_frame, values=["active", "completed", "cancelled"], width=150, state="readonly")
        self.goal_status.set("active")
        self.goal_status.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(add_frame, text="Прогресс (%):").grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.goal_progress = ctk.CTkEntry(add_frame, width=100)
        self.goal_progress.insert(0, "0")
        self.goal_progress.grid(row=5, column=3, padx=5, pady=5, sticky="w")
        
        # Кнопка добавления
        ctk.CTkButton(add_frame, text="Добавить цель", command=self.add_goal).grid(row=6, column=1, columnspan=2, pady=10)
        
        # Таблица целей
        tree_frame = ctk.CTkFrame(self.goals_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Для таблицы продолжаем использовать ttk.Treeview, так как в customtkinter нет аналога
        from tkinter import ttk
        columns = ("ID", "Сотрудник", "Название", "Срок", "Статус", "Прогресс")
        self.goals_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.goals_tree.heading(col, text=col)
            self.goals_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.goals_tree.yview)
        self.goals_tree.configure(yscrollcommand=scrollbar.set)
        
        self.goals_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопка обновления таблицы
        ctk.CTkButton(self.goals_frame, text="Обновить список", command=self.load_goals).pack(pady=5)
        
        
        # Настройка растягивания
        add_frame.columnconfigure(1, weight=1)
        add_frame.columnconfigure(3, weight=1)

    def setup_valuation_tab(self):
        """Настройка вкладки оценок"""

    def setup_recommendations_tab(self):
        """Настройка вкладки рекомендаций"""


    def load_employees(self):
        """Загрузка списка сотрудников в комбобокс"""
        try:
            employees = self.db.get_all_employees()
            employee_names = [emp['display_name'] for emp in employees]
            self.employee_combo.configure(values=employee_names)
            if employee_names:
                self.employee_combo.set(employee_names[0])
            self.employees_data = employees  # Сохраняем данные для поиска ID
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить сотрудников: {str(e)}")
    
    def get_employee_id_from_name(self, display_name):
        """Получение ID сотрудника по отображаемому имени"""
        for emp in self.employees_data:
            if emp['display_name'] == display_name:
                return emp['id']
        return None
    
    def add_goal(self):
        """Добавление новой цели"""
        if not self.validate_goal_data():
            return
        
        employee_display_name = self.employee_var.get()
        employee_id = self.get_employee_id_from_name(employee_display_name)
        
        if not employee_id:
            messagebox.showerror("Ошибка", "Выберите сотрудника")
            return
        
        success, message = self.db.create_goal(
            employee_id=employee_id,
            title=self.goal_title.get().strip(),
            description=self.goal_description.get('1.0', 'end').strip(),
            expected_result=self.expected_result.get('1.0', 'end').strip(),
            deadline=self.goal_deadline.get().strip(),
            task_link=self.task_link.get().strip(),
            status=self.goal_status.get(),
            progress=int(self.goal_progress.get()),
            created_by=self.current_user['id']
        )
        
        if success:
            messagebox.showinfo("Успех", message)
            self.clear_form()
            self.load_goals()
        else:
            messagebox.showerror("Ошибка", message)

    def validate_goal_data(self):
        """Валидация данных цели"""
        if not self.employee_var.get():
            messagebox.showwarning("Предупреждение", "Выберите сотрудника")
            return False
        
        if not self.goal_title.get().strip():
            messagebox.showwarning("Предупреждение", "Введите название цели")
            return False
        
        if not self.expected_result.get('1.0', 'end').strip():
            messagebox.showwarning("Предупреждение", "Введите ожидаемый результат")
            return False
        
        if not self.goal_deadline.get().strip():
            messagebox.showwarning("Предупреждение", "Введите срок выполнения")
            return False
        
        try:
            progress = int(self.goal_progress.get())
            if progress < 0 or progress > 100:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Предупреждение", "Прогресс должен быть числом от 0 до 100")
            return False
        
        return True
    
    def clear_form(self):
        """Очистка формы"""
        self.selected_goal_id = None
        if self.employees_data:
            self.employee_combo.set(self.employees_data[0]['display_name'])
        self.goal_title.delete(0, 'end')
        self.goal_description.delete('1.0', 'end')
        self.expected_result.delete('1.0', 'end')
        self.goal_deadline.delete(0, 'end')
        self.task_link.delete(0, 'end')
        self.goal_status.set("active")
        self.goal_progress.delete(0, 'end')
        self.goal_progress.insert(0, "0")
        
        # Снимаем выделение с таблицы
        for item in self.goals_tree.selection():
            self.goals_tree.selection_remove(item)

    def load_goals(self):
        """Загрузка целей в таблицу"""
        try:
            # Очищаем таблицу
            for item in self.goals_tree.get_children():
                self.goals_tree.delete(item)
            
            # Получаем цели из базы данных
            goals = self.db.get_all_goals()
            goals = self.db.get_all_goals(user_id=self.current_user['id'], user_role='admin')
            
            # Заполняем таблицу
            for goal in goals:
                self.goals_tree.insert("", "end", values=(
                    goal['id'],
                    goal['employee_name'],
                    goal['title'],
                    goal['deadline'],
                    goal['status'],
                    f"{goal['progress']}%"
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить цели: {str(e)}")
    
    def logout(self):
        """Выход из системы"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выйти?"):
            self.root.destroy()