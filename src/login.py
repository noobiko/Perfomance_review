import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, root, auth_manager, on_login_success):
        self.root = root
        self.auth_manager = auth_manager
        self.on_login_success = on_login_success
        self.create_login_window()
    
    def create_login_window(self):
        """Создание окна авторизации"""
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Авторизация")
        self.login_window.geometry("400x400")
        self.login_window.resizable(False, False)
        self.login_window.transient(self.root)
        self.login_window.grab_set()
        
        self.center_window(self.login_window)
        
        login_frame = ttk.LabelFrame(self.login_window, text="Вход в систему", padding=20)
        login_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(login_frame, text="Имя пользователя:").pack(anchor='w', pady=(0, 5))
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.pack(fill='x', pady=(0, 15))
        self.username_entry.focus()
        
        ttk.Label(login_frame, text="Пароль:").pack(anchor='w', pady=(0, 5))
        self.password_entry = ttk.Entry(login_frame, width=30, show="*")
        self.password_entry.pack(fill='x', pady=(0, 20))
        
        ttk.Button(login_frame, text="Войти", command=self.login).pack(fill='x', pady=(0, 10))
        
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