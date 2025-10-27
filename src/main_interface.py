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
        #self.load_employees()
    
    def create_interface(self):
        """Создание основного интерфейса"""
        self.create_menu()
        
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.goals_frame = self.notebook.add("Цели")
        
        self.setup_goals_tab()
    
    def create_menu(self):
        """Создание меню"""
        menubar = ctk.CTkFrame(self.root, height=30)
        menubar.pack(fill='x', padx=10, pady=5)
        
        user_menu = ctk.CTkButton(menubar, text=f"Пользователь ({self.current_user['username']})", 
                                 command=self.logout, width=200)
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
        #ctk.CTkButton(add_frame, text="Добавить цель", command=self.add_goal).grid(row=6, column=1, columnspan=2, pady=10)
        
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
        
        # Кнопка обновления
        #ctk.CTkButton(self.goals_frame, text="Обновить список", command=self.load_goals).pack(pady=5)
        
        # Настройка растягивания
        add_frame.columnconfigure(1, weight=1)
        add_frame.columnconfigure(3, weight=1)
    
    def logout(self):
        """Выход из системы"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выйти?"):
            self.root.destroy()