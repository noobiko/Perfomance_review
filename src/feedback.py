import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

class Feedback360:
    def __init__(self, parent, db_manager, current_user):
        self.parent = parent
        self.db = db_manager
        self.current_user = current_user
        self.employees_data = []
        
        self.setup_feedback_tab(self.parent)
        self.load_employees()
    
    def setup_feedback_tab(self, parent_frame):
        """Настройка вкладки для обратной связи"""
        # Преамбула
        preamble = ("Твой коллега выбрал направление задач или задачи, "
                    "над которыми работа(-а) в течение полугода, по результатам "
                    "выполнения которых просит тебя поделиться своей обратной связью.\n\n"
                    "Поделись обратной связью по формату:")
        ctk.CTkLabel(parent_frame, text=preamble, wraplength=600, justify='left').pack(anchor='w', pady=(0, 10))
        
        # Выбор коллег (множественный выбор)
        ctk.CTkLabel(parent_frame, text="Выбери коллег, по которым можешь дать обратную связь:").pack(anchor='w')
        
        self.colleagues_var = tk.StringVar(value=[])
        self.colleagues_listbox = tk.Listbox(parent_frame, listvariable=self.colleagues_var, selectmode='multiple', height=6)
        self.colleagues_listbox.pack(fill='x', pady=5)
        
        # Кнопка выбора коллеги для оценки
        ctk.CTkButton(parent_frame, text="Оценить выбранного коллегу", 
                     command=self.on_select_colleague).pack(pady=10)
        
        # Фрейм для формы оценки (будет заполняться динамически)
        self.feedback_form_frame = ctk.CTkFrame(parent_frame)
        self.feedback_form_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_employees(self):
        """Загрузка списка сотрудников"""
        try:
            self.employees_data = self.db.get_all_employees()
            colleagues = [emp['display_name'] for emp in self.employees_data 
                         if emp['id'] != self.current_user.get('employee_id')]
            
            # Очищаем и заполняем список
            self.colleagues_listbox.delete(0, tk.END)
            for c in colleagues:
                self.colleagues_listbox.insert('end', c)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить сотрудников: {str(e)}")
    
    def on_select_colleague(self):
        """Обработка выбора коллеги для оценки"""
        selected = self.colleagues_listbox.curselection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите коллегу для оценки")
            return
        
        colleague_name = self.colleagues_listbox.get(selected[0])
        self.show_task_feedback_form(colleague_name)
    
    def show_task_feedback_form(self, colleague_name):
        """Показ формы оценки для выбранного коллеги"""
        # Очистка предыдущей формы
        for widget in self.feedback_form_frame.winfo_children():
            widget.destroy()
    
        # Заголовок с именем коллеги
        ctk.CTkLabel(self.feedback_form_frame, text=f"Оценка коллеги: {colleague_name}",
                     font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))
    
        # Информация о задаче (здесь нужно будет добавить реальные данные)
        task_text = "Текст задачи, связанной с коллегой"
        ctk.CTkLabel(self.feedback_form_frame, text=f"Задача: {task_text}", wraplength=600, justify="left"
                     ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 15))
    
        # 1. Балл достижения результата
        ctk.CTkLabel(self.feedback_form_frame, text="1. Насколько удалось достичь результатов по задаче (0-10):"
                     ).grid(row=2, column=0, sticky="w", pady=5)
        self.result_score = ctk.CTkEntry(self.feedback_form_frame, width=150)
        self.result_score.grid(row=3, column=0, sticky="w", pady=5, padx=(0, 20))
    
        # 2. Личные качества (текст)
        ctk.CTkLabel(self.feedback_form_frame, text="2. Прокомментируй, какие личные качества помогли коллеге достичь результата:"
                     ).grid(row=4, column=0, sticky="nw", pady=5)
        self.personal_qualities = ctk.CTkTextbox(self.feedback_form_frame, width=600, height=80)
        self.personal_qualities.grid(row=5, column=0, columnspan=4, sticky="we", pady=5)
    
        # 3. Качество взаимодействия (балл)
        ctk.CTkLabel(self.feedback_form_frame, text="3. Оцени качество взаимодействия (0-10):"
                     ).grid(row=6, column=0, sticky="w", pady=5)
        self.interaction_score = ctk.CTkEntry(self.feedback_form_frame, width=150)
        self.interaction_score.grid(row=7, column=0, sticky="w", pady=5, padx=(0, 20))
    
        # 4. Рекомендации по улучшению (текст)
        ctk.CTkLabel(self.feedback_form_frame, text="4. Что сотрудник может улучшить в своей работе по задаче в следующее полугодие:"
                     ).grid(row=8, column=0, sticky="nw", pady=5)
        self.improvement_recommendations = ctk.CTkTextbox(self.feedback_form_frame, width=600, height=80)
        self.improvement_recommendations.grid(row=9, column=0, columnspan=4, sticky="we", pady=5)
    
        # Кнопка сохранения оценки
        ctk.CTkButton(self.feedback_form_frame, text="Сохранить обратную связь", 
                     command=lambda: self.save_peer_feedback(colleague_name)
                     ).grid(row=10, column=0, columnspan=4, sticky="w", pady=(20, 0))
    
        # Настройка растяжения колонок
        for col in range(4):
            self.feedback_form_frame.columnconfigure(col, weight=1)
    
    def save_peer_feedback(self, colleague_name):
        """Сохранение обратной связи"""
        try:
            # Здесь будет логика сохранения в базу данных
            messagebox.showinfo("Успех", f"Обратная связь для {colleague_name} сохранена")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить обратную связь: {str(e)}")