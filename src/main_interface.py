import customtkinter as ctk
from tkinter import messagebox
from tkinter import Text
import sqlite3

import llm_recommend
from profile_page import ProfilePage
from llm_set_window import LlmSetWindow

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
        
        self.profile_frame = self.notebook.add("Профиль")
        self.goals_frame = self.notebook.add("Добавить цель")
        self.valuation_frame = self.notebook.add("Оценки")
        self.recommendations_frame = self.notebook.add("Рекомендации")
        
        self.setup_profile_tab()
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
        """Настройка вкладки добавления целей"""
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

        # Вкладка рекомендаций
        self.recommendations_frame.grid_columnconfigure(0, weight=1)
        # self.recommendations_frame.grid_rowconfigure(0, weight=1)
        # self.recommendations_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.recommendations_frame, text="Нейросеть:").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        options = ["GigaChat"]
        self.llm_select = ctk.CTkComboBox(master=self.recommendations_frame, values=options)
        self.llm_select.set("GigaChat")
        self.llm_select.grid(row=1, column=0, pady=5, padx=5)
        ctk.CTkButton(self.recommendations_frame, text="Настройки", command=self.show_llm_settings).grid(row=2, column=0,
                                                                                                  padx=5, pady=5)

        ctk.CTkLabel(self.recommendations_frame, text="Текст запроса:").grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.promt_to_ai = ctk.CTkTextbox(self.recommendations_frame, height=150, undo=True)
        self.promt_to_ai.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        self.promt_to_ai.insert(0.0, "Дай рекоммендацию сотруднику на основании следующих данных: ")

        (ctk.CTkButton(self.recommendations_frame, text="Получить рекомендацию", command=self.get_recommendation).
         grid(row=5, column=0, columnspan=2, pady=5))

        ctk.CTkLabel(self.recommendations_frame, text="Рекомендация:").grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        self.recommendation = ctk.CTkTextbox(self.recommendations_frame, height=400, undo=True)
        self.recommendation.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

    def setup_valuation_tab(self):
        add_frame = ctk.CTkFrame(self.valuation_frame)
        add_frame.pack(fill='x', padx=10, pady=5)

        # Выбор сотрудника для оценки
        ctk.CTkLabel(add_frame, text="ФИО сотрудника:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.valuation_employee_var = ctk.StringVar()
        self.valuation_employee_combo = ctk.CTkComboBox(add_frame, variable=self.valuation_employee_var, width=300,
                                                        state="readonly")
        self.valuation_employee_combo.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="we")
        employee_names = [emp['display_name'] for emp in getattr(self, 'employees_data', [])]
        self.valuation_employee_combo.configure(values=employee_names)
        if employee_names:
            self.valuation_employee_combo.set(employee_names[0])

        # Вопрос 1: Насколько сотруднику удалось достичь результатов
        ctk.CTkLabel(add_frame, text="Насколько сотруднику удалось достичь результатов (0-10):").grid(row=8, column=0,
                                                                                                      padx=5, pady=5,
                                                                                                      sticky="w")
        self.result_score = ctk.CTkEntry(add_frame, width=150)
        self.result_score.grid(row=9, column=0, columnspan=4, padx=5, pady=5, sticky="w")  # Сделано по всей ширине

        # Вопрос 2: Личные качества
        ctk.CTkLabel(add_frame, text="Прокомментируй, какие личные качества помогли коллеге достичь результата:").grid(
            row=2, column=0, padx=5, pady=5, sticky="nw")
        self.personal_qualities = Text(add_frame, width=80, height=4, wrap="word")
        self.personal_qualities.grid(row=3, column=0, columnspan=4, padx=5, pady=5,
                                     sticky="we")  # Выровнено по всей ширине

        # Вопрос 3: Личный вклад
        ctk.CTkLabel(add_frame, text="Что мог бы сделать для улучшения результата:").grid(row=4, column=0, padx=5,
                                                                                          pady=5, sticky="nw")
        self.personal_contribution = Text(add_frame, width=80, height=4, wrap="word")
        self.personal_contribution.grid(row=5, column=0, columnspan=4, padx=5, pady=5,
                                        sticky="we")  # Выровнено по всей ширине

        # Вопрос 5: Рекомендации
        ctk.CTkLabel(add_frame, text="Что бы вы порекомендовали для улучшения в следующем цикле:").grid(row=6, column=0,
                                                                                                        padx=5, pady=5,
                                                                                                        sticky="nw")
        self.improvement_recommendations = Text(add_frame, width=80, height=4, wrap="word")
        self.improvement_recommendations.grid(row=7, column=0, columnspan=4, padx=5, pady=5,
                                              sticky="we")  # Выровнено по всей ширине

        # Вопрос 6: Общий рейтинг (расположить внизу, по 2 на строке)
        ctk.CTkLabel(add_frame, text="Общий рейтинг (0-10):").grid(row=8, column=2, padx=5, pady=5, sticky="w")
        self.overall_rating = ctk.CTkEntry(add_frame, width=150)
        self.overall_rating.grid(row=9, column=2, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(add_frame, text="Оцените качество взаимодействия (0-10):").grid(row=8, column=1, padx=5, pady=5,
                                                                                     sticky="w")
        self.interaction_score = ctk.CTkEntry(add_frame, width=150)
        self.interaction_score.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # Кнопка добавления
        ctk.CTkButton(add_frame, text="Сохранить", command=self.add_goal).grid(row=12, column=0,  padx=5, pady=5, sticky="w")

        # Настройка растягивания колонок
        add_frame.columnconfigure(0, weight=1)
        add_frame.columnconfigure(1, weight=1)
        add_frame.columnconfigure(2, weight=1)
        add_frame.columnconfigure(3, weight=1)

    def setup_recommendations_tab(self):
        """Настройка вкладки рекомендаций"""

    def setup_profile_tab(self):
        """Настройка вкладки профиль"""
        self.profile_page = ProfilePage(self.profile_frame, self.db, self.current_user)

    def load_employees(self):
        """Загрузка списка сотрудников в комбобокс"""
        try:
            employees = self.db.get_all_employees()
            employee_names = [emp['display_name'] for emp in employees]
            self.employee_combo.configure(values=employee_names)
            if employee_names:
                self.employee_combo.set(employee_names[0])
            self.employees_data = employees  
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
            for item in self.goals_tree.get_children():
                self.goals_tree.delete(item)
            
            goals = self.db.get_all_goals()
            goals = self.db.get_all_goals(user_id=self.current_user['id'], user_role='admin')
            
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

    def get_recommendation(self):
        evals = ""

        if self.llm_select.get() == "GigaChat":
            user_message = self.promt_to_ai.get(0.0, 'end') + evals
            answer = llm_recommend.get_chat_completion(llm_recommend.get_giga_token(), user_message)

            if isinstance(answer, Exception):
                self.recommendation.delete(0.0, 'end')
                self.recommendation.insert(0.0, f"Произошла ошибка: {str(answer)}")
            else:
                answer.json()
                result = answer.json()['choices'][0]['message']['content']

                self.recommendation.delete(0.0, 'end')
                self.recommendation.insert(0.0, result.strip())
                # print(result)

    def load_goal_for_editing(self, goal_id):
        """Загрузка цели для редактирования"""
        try:
            goals = self.db.get_all_goals(user_id=self.current_user['id'], user_role=self.current_user['role'])
            
            selected_goal = None
            for goal in goals:
                if goal['id'] == goal_id:
                    selected_goal = goal
                    break
            
            if not selected_goal:
                messagebox.showerror("Ошибка", "Цель не найдена")
                return
            
            self.selected_goal_id = goal_id
        
            employee_display_name = None
            for emp in self.employees_data:
                if emp['id'] == selected_goal['employee_id']:
                    employee_display_name = emp['display_name']
                    break
            
            if employee_display_name:
                self.employee_combo.set(employee_display_name)
            
            self.goal_title.delete(0, 'end')
            self.goal_title.insert(0, selected_goal['title'])
            
            self.goal_description.delete('1.0', 'end')
            self.goal_description.insert('1.0', selected_goal['description'] or '')
            
            self.expected_result.delete('1.0', 'end')
            self.expected_result.insert('1.0', selected_goal['expected_result'] or '')
            
            self.goal_deadline.delete(0, 'end')
            self.goal_deadline.insert(0, selected_goal['deadline'])
            
            self.task_link.delete(0, 'end')
            self.task_link.insert(0, selected_goal['task_link'] or '')
            
            self.goal_status.set(selected_goal['status'])
            
            self.goal_progress.delete(0, 'end')
            self.goal_progress.insert(0, str(selected_goal['progress']))
            
            # Меняем текст кнопки на "Обновить цель"
            # Нужно добавить кнопку обновления в интерфейс или изменить существующую
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить цель для редактирования: {str(e)}")

    def show_llm_settings(self):
        LlmSetWindow(self.root)

    def logout(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выйти?"):
            self.root.destroy()