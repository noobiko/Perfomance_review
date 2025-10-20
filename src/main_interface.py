import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Text
import sqlite3

class MainInterface:
    def __init__(self, root, db_manager, analyzer, current_user):
        self.root = root
        self.db = db_manager
        self.analyzer = analyzer
        self.current_user = current_user
        
        self.create_interface()
        self.load_employees()
    
    def create_interface(self):
        """Создание основного интерфейса"""
        self.create_menu()
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.goals_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.goals_frame, text="Цели")
        
        self.setup_goals_tab()
    
    def create_menu(self):
        """Создание меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        user_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=f"Пользователь ({self.current_user['username']})", menu=user_menu)
        user_menu.add_command(label="Выйти", command=self.logout)

    def setup_goals_tab(self):
        """Настройка вкладки целей"""
        add_frame = ttk.LabelFrame(self.goals_frame, text="Добавить цель", padding=10)
        add_frame.pack(fill='x', padx=10, pady=5)
        
        # Выбор сотрудника
        ttk.Label(add_frame, text="Сотрудник:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.employee_var = tk.StringVar()
        self.employee_combo = ttk.Combobox(add_frame, textvariable=self.employee_var, width=30, state="readonly")
        self.employee_combo.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        
        # Основные поля
        ttk.Label(add_frame, text="Название цели:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.goal_title = ttk.Entry(add_frame, width=60)
        self.goal_title.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        
        ttk.Label(add_frame, text="Описание:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.goal_description = Text(add_frame, width=60, height=3, wrap="word")
        self.goal_description.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        
        ttk.Label(add_frame, text="Ожидаемый результат:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.expected_result = Text(add_frame, width=60, height=3, wrap="word")
        self.expected_result.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        
        # Срок и ссылка
        ttk.Label(add_frame, text="Срок (ГГГГ-ММ-ДД):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.goal_deadline = ttk.Entry(add_frame, width=15)
        self.goal_deadline.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(add_frame, text="Ссылка на задачу:").grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.task_link = ttk.Entry(add_frame, width=30)
        self.task_link.grid(row=4, column=3, padx=5, pady=5, sticky="we")
        
        # Статус и прогресс
        ttk.Label(add_frame, text="Статус:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.goal_status = ttk.Combobox(add_frame, values=["active", "completed", "cancelled"], width=15, state="readonly")
        self.goal_status.set("active")
        self.goal_status.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(add_frame, text="Прогресс (%):").grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.goal_progress = ttk.Spinbox(add_frame, from_=0, to=100, width=10)
        self.goal_progress.set(0)
        self.goal_progress.grid(row=5, column=3, padx=5, pady=5, sticky="w")
        
        # Кнопка добавления
        ttk.Button(add_frame, text="Добавить цель", command=self.add_goal).grid(row=6, column=1, columnspan=2, pady=10)
        
        # Таблица целей
        tree_frame = ttk.Frame(self.goals_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("ID", "Сотрудник", "Название", "Срок", "Статус", "Прогресс")
        self.goals_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.goals_tree.heading(col, text=col)
            self.goals_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.goals_tree.yview)
        self.goals_tree.configure(yscrollcommand=scrollbar.set)
        
        self.goals_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопка обновления
        ttk.Button(self.goals_frame, text="Обновить список", command=self.load_goals).pack(pady=5)
        
        # Настройка растягивания
        add_frame.columnconfigure(1, weight=1)
        add_frame.columnconfigure(3, weight=1)
    
    def logout(self):
        """Выход из системы"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выйти?"):
            self.root.destroy()