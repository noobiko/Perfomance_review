import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class SelfAssessment:
    def __init__(self, parent, db_manager, current_user):
        self.parent = parent
        self.db = db_manager
        self.current_user = current_user

        self.setup_self_assessment_tab(self.parent)
        self.load_tasks()
        
    def setup_self_assessment_tab(self, parent_frame):
        """Настройка вкладки самооценки с шаблонами ответов и оценками"""
        ctk.CTkLabel(parent_frame, text="Опиши результат по задаче:",
                      font=ctk.CTkFont(size=16, weight="bold")).pack(anchor='w', pady=2, padx=10)

        # Пример описания результатов (описание текста вставлено как подсказка)
        examples_result = ()
        ctk.CTkLabel(parent_frame, text=examples_result, justify='left', wraplength=700, text_color='gray').pack(
            anchor='w', padx=10)

        ctk.CTkLabel(parent_frame, text="Выберите задачу:").pack(anchor='w', padx=10, pady=(15, 0))

        task_names = [task['task_name'] for task in getattr(self, 'tasks_data', [])]
        self.task_var = ctk.StringVar()
        self.task_combo = ctk.CTkComboBox(parent_frame, variable=self.task_var,
                                              values=task_names, state="readonly", width=300)
        self.task_combo.pack(anchor='w', pady=5, padx=10)
        if task_names:
            self.task_combo.set(task_names[0])

            # Тексты ответов по пунктам 1-4 из шаблона

        questions_and_prompts = [
            ("1. Впиши, используя шаблон, каких результатов удалось достичь", ""),
            (
                "2. Какой личный вклад ты сделал в полученный результат (пример: благодаря созданной документации команда находила решения в 1,5 раза быстрее)",
            (
            )),
            (
                "3. Что ты забираешь с собой по результатам выполнения этой задачи (например: прокачался в микросервисах, хочу это развивать дальше)",
            ""),
            ("4. Что в следующий раз будешь делать по-другому", "")
        ]

        self.text_widgets = {}
        for i, (question, example) in enumerate(questions_and_prompts):
            ctk.CTkLabel(parent_frame, text=f"{question}").pack(anchor='w', padx=10,
                                                                                pady=(15 if i > 0 else 25, 0))
            if example:
                ctk.CTkLabel(parent_frame, text=example, justify='left', wraplength=700, text_color='gray').pack(
                    anchor='w', padx=20, pady=5)
            textbox = ctk.CTkTextbox(parent_frame, width=700, height=20)
            textbox.pack(fill='x', padx=10, pady=5)
            self.text_widgets[f"text_{i + 1}"] = textbox

        container = ctk.CTkFrame(parent_frame)
        container.pack(fill='x', padx=10, pady=(15, 0))

        # Первая строка, первый столбец - метка с вопросом
        ctk.CTkLabel(container,
                     text="Как ты оцениваешь качество своего взаимодействия с коллегами, командой по данной задаче (0-10):"
                     ).grid(row=0, column=0, sticky='w')

        # Поле ввода для оценки взаимодействия в первом ряду, третий столбец
        self.score_interaction = ctk.CTkEntry(container, width=80)
        self.score_interaction.grid(row=0, column=2, sticky='w', padx=(10, 0))

        # Вторая строка, первый столбец - метка с другим вопросом
        ctk.CTkLabel(container,
                     text="Как ты оцениваешь общую удовлетворённость своим выполнением данной задачи (0-10):"
                     ).grid(row=1, column=0, sticky='w', pady=(20, 0))

        # Поле ввода для оценки удовлетворённости во второй строке, третий столбец
        self.overall_satisfaction = ctk.CTkEntry(container, width=80)
        self.overall_satisfaction.grid(row=1, column=2, sticky='w', pady=(20, 0))
        # Ссылка на рабочее пространство (пункт 3 функционала)
        ctk.CTkLabel(parent_frame,
                     text="Прикрепи ссылку на рабочее пространство, где можно увидеть прогресс по задаче").pack(
            anchor='w', padx=10, pady=(15, 0))
        self.workspace_link = ctk.CTkEntry(parent_frame, width=700)
        self.workspace_link.pack(anchor='w', padx=10, pady=5)

        ctk.CTkButton(parent_frame, text="Сохранить самооценку",
                          command=self.save_self_assessment).pack(pady=20, padx=10)
        

    def load_tasks(self):
        """Загрузка списка задач в комбобокс"""
        try:
            all_tasks = self.db.get_all_tasks()
            task_names = [task['task_name'] for task in all_tasks]
            self.task_combo.configure(values=task_names)
            if task_names:
                self.task_combo.set(task_names[0])
            self.tasks_data = all_tasks  # Сохраняем данные задач для дальнейшего использования
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить задачи: {str(e)}")

    def save_self_assessment(self):
        """Сохранение самооценки в базу данных"""
        try:
            # Получаем выбранную задачу
            selected_task_name = self.task_var.get()
            task_id = None
            for task in self.tasks_data:
                if task['task_name'] == selected_task_name:
                    task_id = task['task_id']
                    break
            
            if not task_id:
                messagebox.showerror("Ошибка", "Выберите задачу")
                return

            # Получаем данные из текстовых полей
            result_description = self.text_widgets["text_1"].get("1.0", "end-1c").strip()
            personal_contribution = self.text_widgets["text_2"].get("1.0", "end-1c").strip()
            lessons_learned = self.text_widgets["text_3"].get("1.0", "end-1c").strip()
            improvements_next_time = self.text_widgets["text_4"].get("1.0", "end-1c").strip()

            # Получаем оценки
            score_interaction = self.score_interaction.get().strip()
            overall_satisfaction = self.overall_satisfaction.get().strip()
            workspace_link = self.workspace_link.get().strip()

            # Валидация данных
            if not all([result_description, personal_contribution, lessons_learned, improvements_next_time]):
                messagebox.showwarning("Предупреждение", "Заполните все текстовые поля")
                return

            try:
                score_interaction = float(score_interaction) if score_interaction else 0.0
                overall_satisfaction = float(overall_satisfaction) if overall_satisfaction else 0.0
                
                if not (0 <= score_interaction <= 10) or not (0 <= overall_satisfaction <= 10):
                    messagebox.showwarning("Предупреждение", "Оценки должны быть в диапазоне от 0 до 10")
                    return
            except ValueError:
                messagebox.showwarning("Предупреждение", "Оценки должны быть числами")
                return

            # Сохраняем в базу данных
            success, message = self.db.create_self_assessment(
                employee_id=self.current_user.get('employee_id'),
                task_id=task_id,
                result_description=result_description,
                personal_contribution=personal_contribution,
                lessons_learned=lessons_learned,
                improvements_next_time=improvements_next_time,
                score_interaction=score_interaction,
                overall_satisfaction=overall_satisfaction,
                workspace_link=workspace_link
            )

            if success:
                messagebox.showinfo("Успех", message)
                self.clear_form()
            else:
                messagebox.showerror("Ошибка", message)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить самооценку: {str(e)}")

    def clear_form(self):
        """Очистка формы после сохранения"""
        # Очищаем текстовые поля
        for text_widget in self.text_widgets.values():
            text_widget.delete("1.0", "end")
        
        # Очищаем поля оценок
        self.score_interaction.delete(0, "end")
        self.overall_satisfaction.delete(0, "end")
        self.workspace_link.delete(0, "end")