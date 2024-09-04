import tkinter as tk
from tkinter import messagebox
import json

# Save score to a file
def save_score(score):
    try:
        with open("scores.json", "r") as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    scores.append(score)
    with open("scores.json", "w") as file:
        json.dump(scores, file)

# Load scores from a file
def load_scores():
    try:
        with open("scores.json", "r") as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []
    return scores

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("400x300")
        self.root.configure(bg="white")  # Set the background color to white
        self.score = 0
        self.current_question = 0
        self.time_per_question = 10
        self.quiz_data = [
            {
                "question": "What is the capital of France?",
                "options": ["A. London", "B. Berlin", "C. Paris", "D. Rome"],
                "answer": "C"
            },
            {
                "question": "What is the largest planet in our solar system?",
                "options": ["A. Earth", "B. Mars", "C. Jupiter", "D. Saturn"],
                "answer": "C"
            },
            {
                "question": "What is the boiling point of water?",
                "options": ["A. 90°C", "B. 100°C", "C. 110°C", "D. 120°C"],
                "answer": "B"
            }
        ]
        self.setup_ui()
        self.show_question()

    def setup_ui(self):
        self.question_label = tk.Label(self.root, text="", wraplength=350, font=("Arial", 14), bg="white", fg="black")
        self.question_label.pack(pady=20)

        self.option_vars = tk.StringVar(value="")
        self.option_buttons = [tk.Radiobutton(self.root, text="", variable=self.option_vars, value=chr(65 + i), font=("Arial", 12), bg="white", fg="black") for i in range(4)]
        for btn in self.option_buttons:
            btn.pack(anchor="w", padx=20, pady=5)

        self.timer_label = tk.Label(self.root, text="", font=("Arial", 12), bg="white", fg="black")
        self.timer_label.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_answer, font=("Arial", 12), bg="blue", fg="white")
        self.submit_button.pack(pady=20)

    def show_question(self):
        question = self.quiz_data[self.current_question]
        self.question_label.config(text=question["question"])
        for i, option in enumerate(question["options"]):
            self.option_buttons[i].config(text=option, value=option[0])
        self.option_vars.set("")
        self.start_timer()

    def start_timer(self):
        self.time_left = self.time_per_question
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.submit_answer()

    def submit_answer(self):
        selected_option = self.option_vars.get()
        correct_answer = self.quiz_data[self.current_question]["answer"]
        if selected_option == correct_answer:
            self.score += 1

        self.current_question += 1
        if self.current_question < len(self.quiz_data):
            self.show_question()
        else:
            self.end_quiz()

    def end_quiz(self):
        save_score(self.score)
        scores = load_scores()
        messagebox.showinfo("Quiz Finished", f"You scored {self.score} out of {len(self.quiz_data)}\nScores: {scores}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
