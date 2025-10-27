# main_interface_admin.py
import customtkinter as ctk
from tkinter import messagebox
from tkinter import Text
import sqlite3
from tkinter import ttk

class AdminInterface:
    def __init__(self, root, db_manager, current_user):
        self.root = root
        self.db = db_manager
        self.current_user = current_user
        self.selected_goal_id = None
        
        self.create_interface()
        self.load_employees()
        self.load_goals()
    
    def create_interface(self):
        """Создание интерфейса администратора"""
        self.create_menu()
        
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.goals_frame = self.notebook.add("Управление целями")
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
        """Настройка вкладки управления целями (как в предыдущей версии)"""
        # ... (код из предыдущей версии main_interface.py без изменений)
        # Тот же код что был раньше, но с использованием прав администратора

    def setup_employees_tab(self):
        """Настройка вкладки управления сотрудниками"""
        ctk.CTkLabel(self.employees_frame, text="Управление сотрудниками", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Здесь можно добавить функционал управления сотрудниками
        ctk.CTkLabel(self.employees_frame, text="Функционал управления сотрудниками в разработке", 
                    font=("Arial", 14)).pack(expand=True)

    def setup_users_tab(self):
        """Настройка вкладки управления пользователями"""
        ctk.CTkLabel(self.users_frame, text="Управление пользователями", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Здесь можно добавить функционал управления пользователями
        ctk.CTkLabel(self.users_frame, text="Функционал управления пользователями в разработке", 
                    font=("Arial", 14)).pack(expand=True)

    # ... остальные методы из предыдущей версии main_interface.py
    # (load_employees, load_goals, add_goal, update_goal, delete_goal и т.д.)

    def logout(self):
        """Выход из системы"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выйти?"):
            self.root.destroy()