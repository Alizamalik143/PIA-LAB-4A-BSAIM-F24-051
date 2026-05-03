import tkinter as tk
from tkinter import messagebox, ttk
from app import DecisionApp

class DecisionMakerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Second Brain AI ✨")
        
        # High class aesthetic theme (Dark Indigo Mode)
        self.bg_color = "#1A1A24"
        self.text_color = "#F4F4F9"
        self.primary_color = "#B5E2FA"
        self.accent_color = "#EDDEA4"
        self.danger_color = "#FF707A"
        
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=self.bg_color)
        
        self.app = DecisionApp()
        self.current_user = None
        self.create_login_frame()

    def toggle_fullscreen(self, event=None):
        is_full = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_full)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- Login Screen ---
    def create_login_frame(self):
        self.clear_frame()
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True)

        tk.Label(
            main_frame, text="🧠 SECOND BRAIN AI", 
            font=("Courier", 44, "bold"), bg=self.bg_color, fg=self.text_color
        ).pack(pady=20)
        
        tk.Label(
            main_frame, text="✨ Make decisions with the vibe you deserve ✨", 
            font=("Helvetica", 18, "italic"), bg=self.bg_color, fg=self.primary_color
        ).pack(pady=10)

        input_frame = tk.Frame(main_frame, bg=self.bg_color, pady=25)
        input_frame.pack()

        tk.Label(
            input_frame, text="USERNAME", 
            font=("Courier", 14, "bold"), bg=self.bg_color, fg=self.text_color
        ).pack(anchor='w', pady=(5, 5))
        
        self.username_entry = tk.Entry(input_frame, width=35, font=("Helvetica", 16), bd=0, relief="flat", bg="#2D2D44", fg=self.text_color)
        self.username_entry.pack(pady=(0, 20), ipady=10)

        tk.Label(
            input_frame, text="PASSWORD", 
            font=("Courier", 14, "bold"), bg=self.bg_color, fg=self.text_color
        ).pack(anchor='w', pady=(5, 5))
        
        self.password_entry = tk.Entry(input_frame, show="*", width=35, font=("Helvetica", 16), bd=0, relief="flat", bg="#2D2D44", fg=self.text_color)
        self.password_entry.pack(pady=(0, 30), ipady=10)

        btn = tk.Button(
            main_frame, text="LET'S GO 🚀", command=self.handle_login_register,
            bg=self.primary_color, fg="#1A1A24", font=("Courier", 16, "bold"),
            bd=0, relief="flat", padx=35, pady=16, cursor="hand2"
        )
        btn.pack(pady=15)
        
        exit_btn = tk.Button(
            main_frame, text="EXIT ❌", command=self.root.destroy,
            bg=self.danger_color, fg="#1A1A24", font=("Courier", 12, "bold"),
            bd=0, relief="flat", padx=20, pady=8, cursor="hand2"
        )
        exit_btn.pack(pady=10)

    def handle_login_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Vibe Check", "Please fill in all fields! 🛑")
            return

        success, msg = self.app.login_or_register(username, password)
        if success:
            self.current_user = username
            self.create_main_menu()
        else:
            messagebox.showerror("Error", f"Something went wrong: {msg}")

    # --- Dashboard with Tab Buttons ---
    def create_main_menu(self):
        self.clear_frame()

        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True)

        tk.Label(
            frame, text=f"Wassup, {self.current_user}! ✌️", 
            font=("Courier", 36, "bold"), bg=self.bg_color, fg=self.text_color
        ).pack(pady=20)
        
        tk.Label(
            frame, text="Select a situation below to conduct your survey:", 
            font=("Helvetica", 18), bg=self.bg_color, fg=self.primary_color
        ).pack(pady=15)

        categories = self.app.get_categories()
        btn_frame = tk.Frame(frame, bg=self.bg_color)
        btn_frame.pack(pady=30)
        
        for i, cat in enumerate(categories):
            def select_cat(c=cat):
                self.start_survey(c)
                
            b = tk.Button(
                btn_frame, text=cat.upper(), command=select_cat,
                bg="#252538", fg=self.text_color,
                activebackground=self.primary_color, activeforeground="#1A1A24",
                font=("Courier", 14, "bold"), width=45, height=2,
                bd=0, relief="flat", cursor="hand2"
            )
            b.pack(pady=8)

        tk.Button(
            frame, text="LOGOUT 🚪", command=self.create_login_frame,
            bg=self.danger_color, fg="#1A1A24", font=("Courier", 12, "bold"),
            bd=0, relief="flat", padx=20, pady=10, cursor="hand2"
        ).pack(pady=25)

    # --- Survey Frame ---
    def start_survey(self, category_title):
        self.questions = self.app.get_questions_for_category(category_title, num_questions=15)
        self.category_title = category_title
        self.current_q_idx = 0
        self.answers = {}
        self.create_survey_frame()

    def create_survey_frame(self):
        self.clear_frame()
        self.survey_frame = tk.Frame(self.root, bg=self.bg_color)
        self.survey_frame.pack(fill="both", expand=True, padx=100, pady=60)

        back_btn = tk.Button(
            self.survey_frame, text="← DASHBOARD", command=self.create_main_menu,
            bg=self.danger_color, fg="#1A1A24", font=("Courier", 11, "bold"), bd=0, padx=14, pady=8, cursor="hand2"
        )
        back_btn.pack(anchor='w', pady=10)

        self.progress_lbl = tk.Label(
            self.survey_frame, text=f"QUESTION {self.current_q_idx + 1} / {len(self.questions)}", 
            font=("Courier", 12, "bold"), bg=self.bg_color, fg=self.primary_color
        )
        self.progress_lbl.pack(anchor='w', pady=10)

        self.question_text = tk.StringVar()
        lbl_q = tk.Label(
            self.survey_frame, textvariable=self.question_text, wraplength=1000, 
            font=("Helvetica", 20, "bold"), bg=self.bg_color, fg=self.text_color, justify="left"
        )
        lbl_q.pack(pady=25, anchor='w')

        self.options_frame = tk.Frame(self.survey_frame, bg=self.bg_color)
        self.options_frame.pack(fill="x", pady=20)

        self.selected_option = tk.IntVar(value=-1)
        self.load_question_data()

    def load_question_data(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        q = self.questions[self.current_q_idx]
        self.question_text.set(f"{q['id']}. {q['question']}")

        for idx, option in enumerate(q['options']):
            r_btn = tk.Radiobutton(
                self.options_frame, text=option, value=idx, 
                variable=self.selected_option, font=("Helvetica", 16),
                bg=self.bg_color, activebackground=self.bg_color, activeforeground=self.primary_color,
                fg=self.text_color, selectcolor=self.bg_color, anchor='w', justify='left'
            )
            r_btn.pack(fill="x", pady=12)

        nav_frame = tk.Frame(self.survey_frame, bg=self.bg_color)
        nav_frame.pack(pady=50)

        if self.current_q_idx > 0:
            tk.Button(
                nav_frame, text="👈 BACK", command=self.prev_question, 
                width=16, bg="#444", fg="white", font=("Courier", 13, "bold"), bd=0, padx=10, pady=8
            ).pack(side="left", padx=25)

        if self.current_q_idx < len(self.questions) - 1:
            tk.Button(
                nav_frame, text="NEXT 👉", command=self.next_question, 
                width=16, bg=self.primary_color, fg="#1A1A24", font=("Courier", 13, "bold"), bd=0, padx=10, pady=8
            ).pack(side="right", padx=25)
        else:
            tk.Button(
                nav_frame, text="SUBMIT ✅", command=self.submit_survey, 
                width=16, bg=self.accent_color, fg="#1A1A24", font=("Courier", 13, "bold"), bd=0, padx=10, pady=8
            ).pack(side="right", padx=25)

    def next_question(self):
        val = self.selected_option.get()
        if val == -1:
            messagebox.showwarning("Hold Up", "Select an option first! ☝️")
            return
        self.answers[self.current_q_idx] = val
        self.current_q_idx += 1
        self.create_survey_frame()

    def prev_question(self):
        if self.selected_option.get() != -1:
            self.answers[self.current_q_idx] = self.selected_option.get()
        self.current_q_idx -= 1
        self.create_survey_frame()

    # --- Advice Window ---
    def create_advice_frame(self, advice_text):
        self.clear_frame()
        
        advice_frame = tk.Frame(self.root, bg=self.bg_color)
        advice_frame.pack(expand=True, padx=80, pady=60)
        
        tk.Label(
            advice_frame, text="🤖 AI DECISION & ADVICE SUMMARY",
            font=("Courier", 28, "bold"), bg=self.bg_color, fg=self.primary_color
        ).pack(pady=20)
        
        # Wrapped text box with style matching the dark frame
        txt_box = tk.Text(
            advice_frame, wrap="word", width=90, height=14,
            font=("Helvetica", 16), bg="#222233", fg=self.text_color,
            bd=0, relief="flat", padx=15, pady=15
        )
        txt_box.insert(tk.END, advice_text)
        txt_box.config(state="disabled")
        txt_box.pack(pady=30)
        
        tk.Button(
            advice_frame, text="DASHBOARD 🏠", command=self.create_main_menu,
            bg=self.primary_color, fg="#1A1A24", font=("Courier", 14, "bold"),
            bd=0, relief="flat", padx=20, pady=10, cursor="hand2"
        ).pack(pady=20)

    # --- Advice Algorithm & Decision Engine ---
    def submit_survey(self):
        val = self.selected_option.get()
        if val == -1:
            messagebox.showwarning("Hold Up", "Select an option first! ☝️")
            return
        
        self.answers[self.current_q_idx] = val
        
        score, total = self.app.save_result(self.current_user, self.category_title, self.answers, self.questions)

        advice_text = ""
        if "Career" in self.category_title:
            if score > (total * 0.6):
                advice_text = (
                    "Advice from Your Second Brain:-\n\n"
                    "Your responses indicate that you have a high preference for independence, ownership, "
                    "and self-management. The AI suggests pivoting to Freelance / Entrepreneurship.\n\n"
                    "WARNING ⚠️: Ensure you have a financial safety net and emergency fund to cover a 6-month runway."
                )
            else:
                advice_text = (
                    "Advice from Your Second Brain:-\n\n"
                    "Your profile shows a need for stability, clear direction, and a structured environment. "
                    "The AI suggests sticking to a Corporate Professional track to grow systematically.\n\n"
                    "WARNING ⚠️: Ensure you upskill and look for new learning challenges inside the company."
                )
        elif "Financial" in self.category_title:
            if score > (total * 0.6):
                advice_text = (
                    "Advice from Your Second Brain:-\n\n"
                    "You show a high tolerance for risk. The AI recommends moving towards aggressive growth investments "
                    "(like equities, crypto, or startup ventures).\n\n"
                    "WARNING ⚠️: Don't put all your capital in a single high-risk asset without a diverse portfolio."
                )
            else:
                advice_text = (
                    "Advice from Your Second Brain:-\n\n"
                    "Your profile is safety-oriented. The AI suggests a low-risk asset allocation like government bonds, "
                    "fixed deposits, and index funds.\n\n"
                    "WARNING ⚠️: Make sure your returns outpace the current rate of inflation."
                )
        else:
            advice_text = (
                "Advice from Your Second Brain:-\n\n"
                "The AI framework advises scheduling your time blocks efficiently and focusing on health boundaries.\n\n"
                "WARNING ⚠️: Don't sacrifice your mental and physical wellness for short-term productivity."
            )

        self.create_advice_frame(advice_text)

if __name__ == "__main__":
    root = tk.Tk()
    app_gui = DecisionMakerGUI(root)
    root.bind("<F11>", app_gui.toggle_fullscreen)
    root.mainloop()


# import tkinter as tk
# from tkinter import messagebox, ttk
# from app import DecisionApp

# class DecisionMakerGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Second Brain AI ✨")
        
#         # Gen Z Aesthetics Colors - Dark Mode Vibes with Pastel Tones
#         self.bg_color = "#1A1A24"      # Dark Violet / Indigo Base
#         self.text_color = "#F4F4F9"    # Light Ice White
#         self.primary_color = "#B5E2FA" # Pastel Blue
#         self.accent_color = "#EDDEA4"  # Pastel Yellow / Gold
#         self.danger_color = "#FF707A"  # Neon Pink / Pastel Coral
        
#         # Fullscreen Mode
#         self.root.attributes('-fullscreen', True)
#         self.root.configure(bg=self.bg_color)
        
#         self.app = DecisionApp()
#         self.current_user = None
#         self.create_login_frame()

#     def toggle_fullscreen(self, event=None):
#         is_full = self.root.attributes('-fullscreen')
#         self.root.attributes('-fullscreen', not is_full)

#     def clear_frame(self):
#         for widget in self.root.winfo_children():
#             widget.destroy()

#     # --- Login Screen ---
#     def create_login_frame(self):
#         self.clear_frame()
        
#         main_frame = tk.Frame(self.root, bg=self.bg_color)
#         main_frame.pack(expand=True)

#         tk.Label(
#             main_frame, text="🧠 SECOND BRAIN AI", 
#             font=("Courier", 44, "bold"), bg=self.bg_color, fg=self.text_color
#         ).pack(pady=20)
        
#         tk.Label(
#             main_frame, text="✨ Make decisions with the vibe you deserve ✨", 
#             font=("Helvetica", 18, "italic"), bg=self.bg_color, fg=self.primary_color
#         ).pack(pady=10)

#         # Input Fields Container
#         input_frame = tk.Frame(main_frame, bg=self.bg_color, pady=25)
#         input_frame.pack()

#         tk.Label(
#             input_frame, text="USERNAME", 
#             font=("Courier", 14, "bold"), bg=self.bg_color, fg=self.text_color
#         ).pack(anchor='w', pady=(5, 5))
        
#         self.username_entry = tk.Entry(input_frame, width=35, font=("Helvetica", 16), bd=0, relief="flat", bg="#2D2D44", fg=self.text_color)
#         self.username_entry.pack(pady=(0, 20), ipady=10)

#         tk.Label(
#             input_frame, text="PASSWORD", 
#             font=("Courier", 14, "bold"), bg=self.bg_color, fg=self.text_color
#         ).pack(anchor='w', pady=(5, 5))
        
#         self.password_entry = tk.Entry(input_frame, show="*", width=35, font=("Helvetica", 16), bd=0, relief="flat", bg="#2D2D44", fg=self.text_color)
#         self.password_entry.pack(pady=(0, 30), ipady=10)

#         # Login / Register Button
#         btn = tk.Button(
#             main_frame, text="LET'S GO 🚀", command=self.handle_login_register,
#             bg=self.primary_color, fg="#1A1A24", font=("Courier", 16, "bold"),
#             bd=0, relief="flat", padx=35, pady=16, cursor="hand2"
#         )
#         btn.pack(pady=15)
        
#         exit_btn = tk.Button(
#             main_frame, text="EXIT ❌", command=self.root.destroy,
#             bg=self.danger_color, fg="#1A1A24", font=("Courier", 12, "bold"),
#             bd=0, relief="flat", padx=20, pady=8, cursor="hand2"
#         )
#         exit_btn.pack(pady=10)

#     def handle_login_register(self):
#         username = self.username_entry.get().strip()
#         password = self.password_entry.get().strip()

#         if not username or not password:
#             messagebox.showwarning("Vibe Check", "Please fill in all fields! 🛑")
#             return

#         success, msg = self.app.login_or_register(username, password)
#         if success:
#             self.current_user = username
#             self.create_main_menu()
#         else:
#             messagebox.showerror("Error", f"Something went wrong: {msg}")

#     # --- Dashboard with Tab Buttons ---
#     def create_main_menu(self):
#         self.clear_frame()

#         frame = tk.Frame(self.root, bg=self.bg_color)
#         frame.pack(expand=True)

#         tk.Label(
#             frame, text=f"Wassup, {self.current_user}! ✌️", 
#             font=("Courier", 36, "bold"), bg=self.bg_color, fg=self.text_color
#         ).pack(pady=20)
        
#         tk.Label(
#             frame, text="Select a situation below to conduct your survey:", 
#             font=("Helvetica", 18), bg=self.bg_color, fg=self.primary_color
#         ).pack(pady=15)

#         categories = self.app.get_categories()
        
#         # Generate 6 interactive buttons as tabs
#         btn_frame = tk.Frame(frame, bg=self.bg_color)
#         btn_frame.pack(pady=30)
        
#         for i, cat in enumerate(categories):
#             def select_cat(c=cat):
#                 self.start_survey(c)
                
#             b = tk.Button(
#                 btn_frame, text=cat.upper(), command=select_cat,
#                 bg="#252538", fg=self.text_color,
#                 activebackground=self.primary_color, activeforeground="#1A1A24",
#                 font=("Courier", 14, "bold"), width=45, height=2,
#                 bd=0, relief="flat", cursor="hand2"
#             )
#             b.pack(pady=8)

#         tk.Button(
#             frame, text="LOGOUT 🚪", command=self.create_login_frame,
#             bg=self.danger_color, fg="#1A1A24", font=("Courier", 12, "bold"),
#             bd=0, relief="flat", padx=20, pady=10, cursor="hand2"
#         ).pack(pady=25)

#     # --- Survey Frame ---
#     def start_survey(self, category_title):
#         self.questions = self.app.get_questions_for_category(category_title, num_questions=15)
#         self.category_title = category_title
#         self.current_q_idx = 0
#         self.answers = {}
#         self.create_survey_frame()

#     def create_survey_frame(self):
#         self.clear_frame()

#         self.survey_frame = tk.Frame(self.root, bg=self.bg_color)
#         self.survey_frame.pack(fill="both", expand=True, padx=100, pady=60)

#         # Dashboard Top Button
#         back_btn = tk.Button(
#             self.survey_frame, text="← DASHBOARD", command=self.create_main_menu,
#             bg=self.danger_color, fg="#1A1A24", font=("Courier", 11, "bold"), bd=0, padx=14, pady=8, cursor="hand2"
#         )
#         back_btn.pack(anchor='w', pady=10)

#         self.progress_lbl = tk.Label(
#             self.survey_frame, text=f"QUESTION {self.current_q_idx + 1} / {len(self.questions)}", 
#             font=("Courier", 12, "bold"), bg=self.bg_color, fg=self.primary_color
#         )
#         self.progress_lbl.pack(anchor='w', pady=10)

#         self.question_text = tk.StringVar()
#         lbl_q = tk.Label(
#             self.survey_frame, textvariable=self.question_text, wraplength=1000, 
#             font=("Helvetica", 20, "bold"), bg=self.bg_color, fg=self.text_color, justify="left"
#         )
#         lbl_q.pack(pady=25, anchor='w')

#         self.options_frame = tk.Frame(self.survey_frame, bg=self.bg_color)
#         self.options_frame.pack(fill="x", pady=20)

#         self.selected_option = tk.IntVar(value=-1)
#         self.load_question_data()

#     def load_question_data(self):
#         for widget in self.options_frame.winfo_children():
#             widget.destroy()

#         q = self.questions[self.current_q_idx]
#         self.question_text.set(f"{q['id']}. {q['question']}")

#         for idx, option in enumerate(q['options']):
#             r_btn = tk.Radiobutton(
#                 self.options_frame, text=option, value=idx, 
#                 variable=self.selected_option, font=("Helvetica", 16),
#                 bg=self.bg_color, activebackground=self.bg_color, activeforeground=self.primary_color,
#                 fg=self.text_color, selectcolor=self.bg_color, anchor='w', justify='left'
#             )
#             r_btn.pack(fill="x", pady=12)

#         nav_frame = tk.Frame(self.survey_frame, bg=self.bg_color)
#         nav_frame.pack(pady=50)

#         if self.current_q_idx > 0:
#             tk.Button(
#                 nav_frame, text="👈 BACK", command=self.prev_question, 
#                 width=16, bg="#444", fg="white", font=("Courier", 13, "bold"), bd=0, padx=10, pady=8
#             ).pack(side="left", padx=25)

#         if self.current_q_idx < len(self.questions) - 1:
#             tk.Button(
#                 nav_frame, text="NEXT 👉", command=self.next_question, 
#                 width=16, bg=self.primary_color, fg="#1A1A24", font=("Courier", 13, "bold"), bd=0, padx=10, pady=8
#             ).pack(side="right", padx=25)
#         else:
#             tk.Button(
#                 nav_frame, text="SUBMIT ✅", command=self.submit_survey, 
#                 width=16, bg=self.accent_color, fg="#1A1A24", font=("Courier", 13, "bold"), bd=0, padx=10, pady=8
#             ).pack(side="right", padx=25)

#     def next_question(self):
#         val = self.selected_option.get()
#         if val == -1:
#             messagebox.showwarning("Hold Up", "Select an option first! ☝️")
#             return

#         self.answers[self.current_q_idx] = val
#         self.current_q_idx += 1
#         self.create_survey_frame()

#     def prev_question(self):
#         if self.selected_option.get() != -1:
#             self.answers[self.current_q_idx] = self.selected_option.get()

#         self.current_q_idx -= 1
#         self.create_survey_frame()

#     # --- Advice Algorithm & Decision Engine ---
#     def submit_survey(self):
#         val = self.selected_option.get()
#         if val == -1:
#             messagebox.showwarning("Hold Up", "Select an option first! ☝️")
#             return
        
#         self.answers[self.current_q_idx] = val

#         score, total = self.app.save_result(self.current_user, self.category_title, self.answers, self.questions)
        
#         # Advice aur Decision ki conditions
#         if "Career" in self.category_title:
#             if score > (total * 0.6):
#                 advice = (
#                     "🤖 AI Decision Engine Advice:-\n\n"
#                     "Aapka score is baat ki nishandahi karta hai ke aap independent aur autonomous style pasand karte hain. "
#                     "Aapko 'Freelance / Startup' ki taraf jana chahiye! Freedom aur ownership aapke liye best hain.\n\n"
#                     "⚠️ WARNING: Financial runway (at least 6 months) zaroor maintain rakhein!"
#                 )
#             else:
#                 advice = (
#                     "🤖 AI Decision Engine Advice:-\n\n"
#                     "Aapka score ek structured aur stable mahol ki taraf ishara karta hai. "
#                     "Aapko 'Corporate Professional' path choose karna chahie. Stability aapki energy ko improve karegi.\n\n"
#                     "⚠️ WARNING: Routine task se boriyat ho to skilling zaroor jari rakhein!"
#                 )
#         elif "Financial" in self.category_title:
#             if score > (total * 0.6):
#                 advice = (
#                     "🤖 AI Decision Engine Advice:-\n\n"
#                     "Aap high risk lene mein comfortable hain. Growth-oriented investments (jaise stocks ya startups) aapke liye behtar rahengi.\n\n"
#                     "⚠️ WARNING: Aggressive investment mein diversification ka khayal rakhein!"
#                 )
#             else:
#                 advice = (
#                     "🤖 AI Decision Engine Advice:-\n\n"
#                     "Safety-first aur risk-averse approach best hai. Safety funds, FDs, aur real estate jaise stable assets mein invest karein.\n\n"
#                     "⚠️ WARNING: Inflation se bachne k lye real return rate zaroor check karein!"
#                 )
#         else:
#             advice = (
#                 "🤖 AI Decision Engine Advice:-\n\n"
#                 "Second Brain AI ki advice hai ki aap apne daily time-blocking aur balance par tawajah dein. "
#                 "Apne kaam aur personal life ki boundaries define karein.\n\n"
#                 "⚠️ WARNING: Burnout se bachne k lye physical exercise zaroori hai!"
#             )

#         messagebox.showinfo(
#             "🎉 Your Vibe & AI Advice Summary", 
#             f"User: {self.current_user}\nCategory: {self.category_title}\n\n"
#             f"Total Score: {score} / {total}\n\n"
#             f"{advice}"
#         )
#         self.create_main_menu()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app_gui = DecisionMakerGUI(root)
#     root.bind("<F11>", app_gui.toggle_fullscreen)
#     root.mainloop()




