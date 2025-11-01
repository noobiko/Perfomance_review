import customtkinter as ctk
from tkinter import messagebox

class LlmSetWindow:
    def __init__(self, root):
        self.root = root
        # self.auth_manager = auth_manager
        self.create_llm_set_window()

    def create_llm_set_window(self):
        """Создание окна авторизации"""
        self.llm_set_window = ctk.CTkToplevel(self.root)
        self.llm_set_window.title("Настройки")
        self.llm_set_window.geometry("400x400")
        self.llm_set_window.after(250, lambda: self.llm_set_window.iconbitmap('pics/icon.ico'))
        self.llm_set_window.resizable(False, False)
        self.llm_set_window.transient(self.root)
        self.llm_set_window.grab_set()

        self.center_window(self.llm_set_window)

        llm_settings_frame = ctk.CTkFrame(self.llm_set_window)
        llm_settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(llm_settings_frame, text="Настройки API нейросети", font=("Arial", 16, "bold")).pack(pady=(20, 30))

        ctk.CTkLabel(llm_settings_frame, text="RqUID:").pack(anchor='w', pady=(0, 5))
        self.uid_entry = ctk.CTkEntry(llm_settings_frame, width=300)
        self.uid_entry.pack(fill='x', pady=(0, 15))
        self.uid_entry.focus()

        ctk.CTkLabel(llm_settings_frame, text="Authorization:").pack(anchor='w', pady=(0, 5))
        self.auth_entry = ctk.CTkEntry(llm_settings_frame, width=300)
        self.auth_entry.pack(fill='x', pady=(0, 20))

        ctk.CTkButton(llm_settings_frame, text="OK", command=self.get_uid_data).pack(fill='x', pady=(0, 10))

        self.llm_set_window.bind('<Return>', lambda e: self.get_uid_data())
        self.fill_in_entries()

    def center_window(self, window):
        """Центрирование окна"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() - window.winfo_width()) // 2
        y = (window.winfo_screenheight() - window.winfo_height()) // 2
        window.geometry(f"+{x}+{y}")

    def get_uid_data(self):
        uid = self.uid_entry.get().strip()
        auth = self.auth_entry.get().strip()

        if not uid or not auth:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
            return
        else:
            self.llm_set_window.destroy()
            self.save_creds_to_file(uid, auth)

        # success, message, user_data = self.auth_manager.login_user(username, password)
        #
        # if success:
        #     messagebox.showinfo("Успех", message)
        #     self.llm_set_window.destroy()
        # else:
        #     messagebox.showerror("Ошибка", message)

    def fill_in_entries(self):
        with open('creds.txt', 'r') as creds_file:
            uid = creds_file.readline().strip()
            auth = creds_file.readline().strip()

        self.uid_entry.insert(0, uid)
        self.auth_entry.insert(0, auth)

    def save_creds_to_file(self, uid, auth):
        # uid = self.uid_entry.get().strip()
        # auth = self.auth_entry.get().strip()

        with open('creds.txt', 'w') as creds_file:
            creds_file.write(uid + "\n")
            creds_file.write(auth)