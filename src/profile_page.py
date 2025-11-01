import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, db_manager, current_user, main_interface):
        self.parent = parent
        self.db = db_manager
        self.current_user = current_user
        self.selected_goal_id = None
        self.main_interface = main_interface
        
        self.create_widgets()
        self.load_profile_data()
        self.load_user_goals()
    
    def create_widgets(self):
        """Создание виджетов страницы профиля"""
        main_container = ctk.CTkFrame(self.parent)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        left_frame = ctk.CTkFrame(main_container)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        right_frame = ctk.CTkFrame(main_container)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        self.setup_employee_info(left_frame)
        
        self.setup_goals_section(right_frame)
    
    def setup_employee_info(self, parent):
        """Настройка секции с информацией о сотруднике"""
        ctk.CTkLabel(parent, text="Информация о сотруднике", 
                    font=("Arial", 16, "bold")).pack(pady=(10, 20))
        
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.info_labels = {}
        fields = [
            ("ФИО:", "full_name"),
            ("Должность:", "position"),
            ("Отдел:", "department"),
            ("Email:", "email"),
            ("Дата приема:", "hire_date")
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            ctk.CTkLabel(info_frame, text=label_text, font=("Arial", 12, "bold")).grid(
                row=i, column=0, padx=5, pady=8, sticky="w")
            
            value_label = ctk.CTkLabel(info_frame, text="", font=("Arial", 12))
            value_label.grid(row=i, column=1, padx=5, pady=8, sticky="w")
            self.info_labels[field_name] = value_label
        

        info_frame.columnconfigure(1, weight=1)
    
    def setup_goals_section(self, parent):
        """Настройка секции с целями сотрудника"""
        ctk.CTkLabel(parent, text="Текущие цели", 
                    font=("Arial", 16, "bold")).pack(pady=(10, 10))
        
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill='x', padx=10, pady=(0, 10))  
        
        ctk.CTkButton(button_frame, text="Обновить список", 
                    command=self.load_user_goals).pack(side='left', padx=5)
        ctk.CTkButton(button_frame, text="Просмотреть цель", 
                    command=self.view_goal_details).pack(side='left', padx=5)
        
        #btn_goals = ctk.CTkButton(button_frame, text="Создать цель", command=self.go_to_goals)
        #btn_goals.pack()
        ctk.CTkButton(button_frame, text="Создать цель", 
                    command=self.go_to_goals).pack(side='left', padx=5)
        
        tree_frame = ctk.CTkFrame(parent)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("ID", "Название", "Срок", "Статус", "Прогресс")
        self.goals_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        
        column_widths = {"ID": 50, "Название": 200, "Срок": 100, "Статус": 100, "Прогресс": 80}
        for col in columns:
            self.goals_tree.heading(col, text=col)
            self.goals_tree.column(col, width=column_widths[col])
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.goals_tree.yview)
        self.goals_tree.configure(yscrollcommand=scrollbar.set)
        
        self.goals_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        
        self.goals_tree.bind('<Double-1>', lambda e: self.view_goal_details())
        self.goals_tree.bind('<ButtonRelease-1>', self.on_goal_select)
    
    def go_to_goals(self):
        """Создать новую цель"""
        self.main_interface.notebook.set("Добавить цель")

    def load_profile_data(self):
        """Загрузка данных профиля сотрудника"""
        try:
            if self.current_user.get('employee_id'):
                employee = self.db.get_employee_by_user_id(self.current_user['id'])
            else:
                employee = None
            
            if employee:
                self.info_labels['full_name'].configure(
                    text=f"{employee['first_name']} {employee['last_name']}")
                self.info_labels['position'].configure(text=employee['position'])
                self.info_labels['department'].configure(text=employee['department'])
                self.info_labels['email'].configure(text=employee.get('email', 'Не указан'))
                self.info_labels['hire_date'].configure(text=employee.get('hire_date', 'Не указана'))
            else:
                for label in self.info_labels.values():
                    label.configure(text="Не указано")
                messagebox.showinfo("Информация", 
                                  "Ваш профиль пользователя не связан с сотрудником. Обратитесь к администратору.")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные профиля: {str(e)}")
    
    def load_user_goals(self):
        """Загрузка целей текущего пользователя"""
        try:
            for item in self.goals_tree.get_children():
                self.goals_tree.delete(item)
            
            goals = self.db.get_all_goals(user_id=self.current_user['id'], user_role=self.current_user['role'])
            
            if self.current_user['role'] != 'admin' and self.current_user.get('employee_id'):
                user_goals = [goal for goal in goals if goal['employee_id'] == self.current_user['employee_id']]
            else:
                user_goals = goals
            
            for goal in user_goals:
                self.goals_tree.insert("", "end", values=(
                    goal['id'],
                    goal['title'],
                    goal['deadline'],
                    goal['status'],
                    f"{goal['progress']}%"
                ))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить цели: {str(e)}")
    
    def on_goal_select(self, event):
        """Обработка выбора цели в таблице"""
        selected = self.goals_tree.selection()
        if selected:
            self.selected_goal_id = self.goals_tree.item(selected[0])['values'][0]
    
    def view_goal_details(self):
        """Просмотр подробной информации о выбранной цели"""
        if not self.selected_goal_id:
            messagebox.showwarning("Предупреждение", "Выберите цель для просмотра")
            return
        
        try:
            goals = self.db.get_all_goals(user_id=self.current_user['id'], user_role=self.current_user['role'])
            selected_goal = None
            
            for goal in goals:
                if goal['id'] == self.selected_goal_id:
                    selected_goal = goal
                    break
            
            if not selected_goal:
                messagebox.showerror("Ошибка", "Цель не найдена")
                return
            
            self.show_goal_details(selected_goal)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить информацию о цели: {str(e)}")
    
    def show_goal_details(self, goal):
        """Отображение детальной информации о цели"""
        detail_window = ctk.CTkToplevel(self.parent)
        detail_window.title(f"Детали цели: {goal['title']}")
        detail_window.geometry("700x600")  
        detail_window.resizable(True, True)
        detail_window.transient(self.parent)
        detail_window.grab_set()
        detail_window.after(250, lambda: detail_window.iconbitmap('pics/icon.ico'))
 
        
        self.center_window(detail_window)

        scrollable_frame = ctk.CTkScrollableFrame(detail_window)
        scrollable_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(scrollable_frame, text=goal['title'], 
                    font=("Arial", 18, "bold")).pack(pady=(0, 20), fill='x')
        details = [
            ("Сотрудник:", goal['employee_name'], False),
            ("Срок выполнения:", goal['deadline'], False),
            ("Статус:", goal['status'], False),
            ("Прогресс:", f"{goal['progress']}%", False),
            ("Ссылка на задачу:", goal['task_link'] or "Не указана", False),
            ("Описание:", goal['description'] or "Не указано", True),
            ("Ожидаемый результат:", goal['expected_result'] or "Не указано", True)
        ]
        for i, (label, value, is_multiline) in enumerate(details):
            item_frame = ctk.CTkFrame(scrollable_frame)
            item_frame.pack(fill='x', pady=(0, 15))
            ctk.CTkLabel(item_frame, text=label, font=("Arial", 12, "bold")).pack(
                anchor='w', pady=(0, 5))
            if is_multiline:
                text_height = 8 if label == "Описание:" else 10
                text_widget = ctk.CTkTextbox(item_frame, height=text_height, wrap='word')
                text_widget.pack(fill='x', pady=(0, 0))
                text_widget.insert('1.0', value)
                text_widget.configure(state='disabled')
            else:
                value_label = ctk.CTkLabel(item_frame, text=value, font=("Arial", 12))
                value_label.pack(anchor='w', pady=(0, 0))
        button_frame = ctk.CTkFrame(scrollable_frame)
        button_frame.pack(fill='x', pady=20)
        edit_button = ctk.CTkButton(
            button_frame, 
            text="Изменить цель", 
            command=lambda: self.edit_goal(goal['id'], detail_window),
            fg_color="#FF9500",
            hover_color="#E68500"
        )
        edit_button.pack(side='left', padx=(0, 10))
        close_button = ctk.CTkButton(
            button_frame, 
            text="Закрыть", 
            command=detail_window.destroy
        )
        close_button.pack(side='left')

    def edit_goal(self, goal_id, detail_window):
        """Переход к редактированию цели"""
        detail_window.destroy()
        if hasattr(self.parent, 'notebook'):
            self.parent.notebook.set("Цели")
            self.parent.selected_goal_id = goal_id
            self.parent.load_goal_for_editing(goal_id)
        elif hasattr(self.parent.master, 'notebook'):
            self.parent.master.notebook.set("Просмотр целей")
            messagebox.showinfo("Информация", 
                              "Для администратора редактирование целей доступно через основную вкладку просмотра целей")
    def center_window(self, window):
        """Центрирование окна"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() - window.winfo_width()) // 2
        y = (window.winfo_screenheight() - window.winfo_height()) // 2
        window.geometry(f"+{x}+{y}")


        