# login.py
import customtkinter as ctk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, root, auth_manager, on_login_success):
        self.root = root
        self.auth_manager = auth_manager
        self.on_login_success = on_login_success
        self.create_login_window()
    
    def create_login_window(self):
        """Создание окна авторизации"""
        self.login_window = ctk.CTkToplevel(self.root)
        self.login_window.title("Авторизация")
        self.login_window.geometry("400x400")
        self.login_window.resizable(False, False)
        self.login_window.transient(self.root)
        self.login_window.grab_set()
        
        self.center_window(self.login_window)
        
        login_frame = ctk.CTkFrame(self.login_window)
        login_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(login_frame, text="Вход в систему", font=("Arial", 16, "bold")).pack(pady=(20, 30))
        
        ctk.CTkLabel(login_frame, text="Имя пользователя:").pack(anchor='w', pady=(0, 5))
        self.username_entry = ctk.CTkEntry(login_frame, width=300)
        self.username_entry.pack(fill='x', pady=(0, 15))
        self.username_entry.focus()
        
        ctk.CTkLabel(login_frame, text="Пароль:").pack(anchor='w', pady=(0, 5))
        self.password_entry = ctk.CTkEntry(login_frame, width=300, show="*")
        self.password_entry.pack(fill='x', pady=(0, 20))
        
        ctk.CTkButton(login_frame, text="Войти", command=self.login).pack(fill='x', pady=(0, 10))
        
        self.login_window.bind('<Return>', lambda e: self.login())
    
    def center_window(self, window):
        """Центрирование окна"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() - window.winfo_width()) // 2
        y = (window.winfo_screenheight() - window.winfo_height()) // 2
        window.geometry(f"+{x}+{y}")
    
    def login(self):
        """Обработка входа"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
            return
        
        success, message, user_data = self.auth_manager.login_user(username, password)
        
        if success:
            messagebox.showinfo("Успех", message)
            self.login_window.destroy()
            self.on_login_success(user_data)
        else:
            messagebox.showerror("Ошибка", message)