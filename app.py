import tkinter as tk
from tkinter import messagebox
import random

# Base Question class
class Question:
    def __init__(self, prompt, options, answer):
        self._prompt = prompt
        self._options = options
        self._answer = answer

    def get_prompt(self):
        return self._prompt

    def get_options(self):
        return self._options

    def check_answer(self, selected_option):
        return selected_option == self._answer


# Inherited MCQ class
class MCQQuestion(Question):
    def __init__(self, prompt, options, answer):
        super().__init__(prompt, options, answer)


# GUI Logic
class QuizApp:
    def __init__(self, master, questions):
        self.master = master
        self.master.title("OOP Quiz")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg="#f0f8ff")

        self.questions = questions
        self.current_question_index = 0
        self.score = 0
        self.selected_option = tk.StringVar()
        self.time_left = 60  # seconds per question
        self.timer_id = None

        self.create_widgets()
        self.display_question()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="TECH WORLD", font=("Helvetica", 26, "bold"),
                                    bg="#4682b4", fg="white", pady=10)
        self.title_label.pack(fill='x')

        self.subtitle_frame = tk.Frame(self.master, bg="#87cefa")
        self.subtitle_frame.pack(fill='x')

        self.subtitle_label = tk.Label(self.subtitle_frame, text="Object-Oriented Programming Quiz", font=("Helvetica", 20),
                                       bg="#87cefa", fg="black", pady=10)
        self.subtitle_label.pack(side='left', padx=20)

        self.timer_label = tk.Label(self.subtitle_frame, text="", font=("Helvetica", 16),
                                    bg="#87cefa", fg="red")
        self.timer_label.pack(side='right', padx=20)

        self.content_frame = tk.Frame(self.master, bg="#f0f8ff", pady=30)
        self.content_frame.pack(padx=40, fill='both', expand=True)

        self.question_label = tk.Label(self.content_frame, text="", wraplength=800, font=('Arial', 16, "bold"),
                                       bg="#f0f8ff", fg="#333")
        self.question_label.pack(pady=20)

        self.radio_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(self.content_frame, text="", variable=self.selected_option,
                                 value="", font=('Arial', 14), bg="#e6f2ff", anchor='w',
                                 width=40, justify='left', indicatoron=0, padx=10, pady=10,
                                 relief='raised', bd=2, fg="#000080", selectcolor="#cce6ff")
            btn.pack(pady=5, fill='x')
            self.radio_buttons.append(btn)

        self.next_button = tk.Button(self.master, text="Next", command=self.next_question,
                                     font=("Arial", 14), bg="#5cb85c", fg="white", padx=20, pady=10)
        self.next_button.pack(pady=20)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit,
                                     font=("Arial", 12), bg="#d9534f", fg="white")
        self.exit_button.pack(side='bottom', pady=10)

    def display_question(self):
        # Reset timer
        self.time_left = 60
        self.update_timer()

        q = self.questions[self.current_question_index]
        self.question_label.config(text=f"Q{self.current_question_index + 1}: {q.get_prompt()}")
        self.selected_option.set(None)

        options = q.get_options()
        for i, key in enumerate(sorted(options)):
            self.radio_buttons[i].config(text=f"{key.upper()}: {options[key]}", value=key)

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            messagebox.showwarning("Time's Up!", "You didn't answer in time!")
            self.next_question()

    def next_question(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

        selected = self.selected_option.get()
        q = self.questions[self.current_question_index]
        if selected and q.check_answer(selected):
            self.score += 1

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            self.show_result()

    def show_result(self):
        messagebox.showinfo("Quiz Completed", f"Your score: {self.score}/{len(self.questions)}")
        self.master.destroy()


# Questions
question_data = [
    MCQQuestion("What is Encapsulation in OOP?",
                {"a": "Hiding internal details", "b": "Using functions only", "c": "Repeating code", "d": "None of these"},
                "a"),
    MCQQuestion("Which keyword is used for Inheritance in Python?",
                {"a": "inherit", "b": "extends", "c": "super", "d": "class"},
                "d"),
    MCQQuestion("What is Polymorphism?",
                {"a": "Many forms of a function", "b": "Hiding information", "c": "Overriding loops", "d": "None of the above"},
                "a"),
    MCQQuestion("Which principle allows same method name for different classes?",
                {"a": "Encapsulation", "b": "Polymorphism", "c": "Abstraction", "d": "Inheritance"},
                "b"),
    MCQQuestion("What is Abstraction in OOP?",
                {"a": "Writing full details", "b": "Showing only essential features", "c": "Making things public", "d": "All of these"},
                "b")
]

# Run the App
random.shuffle(question_data)
root = tk.Tk()
app = QuizApp(root, question_data)
root.mainloop()
