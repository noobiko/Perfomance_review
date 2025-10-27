# app.py
import customtkinter as ctk
from auth import AuthManager
from database import DatabaseManager
from login import LoginWindow
from main_interface import MainInterface

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления целями сотрудников")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Инициализация компонентов
        self.db = DatabaseManager()
        self.auth_manager = AuthManager(self.db)
        
        # Показать окно авторизации
        self.show_login()
    
    def show_login(self):
        """Показать окно авторизации"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        LoginWindow(self.root, self.auth_manager, self.on_login_success)
    
    def on_login_success(self, user_data):
        """Обработка успешного входа"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Создаем главный интерфейс
        MainInterface(self.root, self.db, user_data)

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApplication(root)
    root.mainloop()