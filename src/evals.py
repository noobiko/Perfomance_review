def create_interface(self):

        self.notebook.add("Самооценка")


        self.self_assessment_frame = self.notebook.tab("Самооценка")



        self.setup_self_assessment_tab(self.self_assessment_frame)

# def setup_feedback_tab(self, user_role):
    #     """Настройка вкладки для обратной связи (руководитель и обычный сотрудник)"""
    #     from tkinter import ttk
    #
    #     feedback_frame = ctk.CTkFrame(self.root)  # или ваше окно/фрейм
    #     feedback_frame.pack(fill='both', expand=True, padx=10, pady=10)
        #
        # # Если роль руководитель, показываем форму оценок руководителя (setup_valuation_tab)
        # if user_role == 'admin':
        #     self.setup_valuation_tab()
        #     return

        # Для обычных сотрудников — форма обратной связи с множественным выбором респондентов

        # # Преамбула
        # preamble = ("Твой коллега выбрал направление задач или задачи, "
        #             "над которыми работа(-а) в течение полугода, по результатам "
        #             "выполнения которых просит тебя поделиться своей обратной связью.\n\n"
        #             "Поделись обратной связью по формату:")
        # ctk.CTkLabel(feedback_frame, text=preamble, wraplength=600, justify='left').pack(anchor='w', pady=(0, 10))
        #
        # # Выбор коллег (множественный выбор)
        # ctk.CTkLabel(feedback_frame, text="Выбери коллег, по которым можешь дать обратную связь:").pack(anchor='w')
        # colleagues = [emp['display_name'] for emp in getattr(self, 'employees_data', []) if
        #               emp['id'] != self.current_user_employee_id]
        # self.colleagues_var = ctk.StringVar(value=[])
        # self.colleagues_listbox = tk.Listbox(feedback_frame, listvariable=self.colleagues_var, selectmode='multiple',
        #                                      height=6)
        # for c in colleagues:
        #     self.colleagues_listbox.insert('end', c)
        # self.colleagues_listbox.pack(fill='x', pady=5)
        #
        # # Кнопка выбора коллеги для оценки (показывает первый выбранный)
        # def on_select_colleague():
        #     selected = self.colleagues_listbox.curselection()
        #     if not selected:
        #         ctk.CTkLabel(feedback_frame, text="Выберите коллегу для оценки.", text_color="red").pack()
        #         return
        #     colleague_name = self.colleagues_listbox.get(selected[0])
        #     self.show_task_feedback_form(feedback_frame, colleague_name)
        #
        # ctk.CTkButton(feedback_frame, text="Оценить выбранного коллегу", command=on_select_colleague).pack(pady=10)

    # def show_task_feedback_form(self, parent_frame, colleague_name):
    #     """Показ формы оценки для выбранного коллеги внутри заданного родителя"""
    #     # Очистка предыдущих виджетов (кроме кнопок и списка, если есть)
    #     for widget in parent_frame.winfo_children():
    #         if isinstance(widget, ctk.CTkButton) or isinstance(widget, tk.Listbox):
    #             continue
    #         widget.destroy()
    #
    #     # Создаем контейнер для формы оценки
    #     add_frame = ctk.CTkFrame(parent_frame)
    #     add_frame.pack(fill='both', expand=True, padx=10, pady=10)
    #
    #     # Заголовок с именем коллеги
    #     ctk.CTkLabel(add_frame, text=f"Оценка коллеги: {colleague_name}",
    #                  font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, sticky="w",
    #                                                                 pady=(0, 15))
    #
    #     # Информация о задаче
    #     task_text = "Текст задачи, связанной с коллегой"
    #     ctk.CTkLabel(add_frame, text=f"Задача: {task_text}", wraplength=600, justify="left"
    #                  ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 15))
    #
    #     # 1. Балл достижения результата
    #     ctk.CTkLabel(add_frame, text="1. Насколько удалось достичь результатов по задаче (0-10):"
    #                  ).grid(row=2, column=0, sticky="w", pady=5)
    #     self.result_score = ctk.CTkEntry(add_frame, width=150)
    #     self.result_score.grid(row=3, column=0, sticky="w", pady=5, padx=(0, 20))
    #
    #     # 2. Личные качества (текст)
    #     ctk.CTkLabel(add_frame, text="2. Прокомментируй, какие личные качества помогли коллеге достичь результата:"
    #                  ).grid(row=4, column=0, sticky="nw", pady=5)
    #     self.personal_qualities = ctk.CTkTextbox(add_frame, width=600, height=80)
    #     self.personal_qualities.grid(row=5, column=0, columnspan=4, sticky="we", pady=5)
    #
    #     # 3. Качество взаимодействия (балл)
    #     ctk.CTkLabel(add_frame, text="3. Оцени качество взаимодействия (0-10):"
    #                  ).grid(row=6, column=0, sticky="w", pady=5)
    #     self.interaction_score = ctk.CTkEntry(add_frame, width=150)
    #     self.interaction_score.grid(row=7, column=0, sticky="w", pady=5, padx=(0, 20))
    #
    #     # 4. Рекомендации по улучшению (текст)
    #     ctk.CTkLabel(add_frame, text="4. Что сотрудник может улучшить в своей работе по задаче в следующее полугодие:"
    #                  ).grid(row=8, column=0, sticky="nw", pady=5)
    #     self.improvement_recommendations = ctk.CTkTextbox(add_frame, width=600, height=80)
    #     self.improvement_recommendations.grid(row=9, column=0, columnspan=4, sticky="we", pady=5)
    #
    #     # Кнопка сохранения оценки
    #     ctk.CTkButton(add_frame, text="Сохранить обратную связь", command=self.save_peer_feedback
    #                   ).grid(row=10, column=0, columnspan=4, sticky="w", pady=(20, 0))
    #
    #     # Настройка растяжения колонок
    #     for col in range(4):
    #         add_frame.columnconfigure(col, weight=1)
    #     for row in range(11):
    #         add_frame.rowconfigure(row, weight=0)
    #
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

        # Дополнительная подсказка (если нужна) рядом в первом ряду, второй столбец
        ctk.CTkLabel(container, font=ctk.CTkFont(size=12),
                     text_color='gray'
                     ).grid(row=0, column=1, sticky='w', padx=(10, 0))

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
