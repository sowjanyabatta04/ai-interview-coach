import tkinter as tk
from tkinter import ttk
import random
from questions import questions
from analyzer import analyze_answer

# Global variables
round_number = 0
total_score = 0
question_list = []

# Window
window = tk.Tk()
window.title("AI Interview Coach")
window.geometry("550x500")

# Title
title = tk.Label(window, text="AI Interview Coach", font=("Arial", 20))
title.pack(pady=10)

# Round Label
round_label = tk.Label(window, text="Round: 0/5", font=("Arial", 12))
round_label.pack()

# Candidate Name
tk.Label(window, text="Candidate Name").pack()
name_entry = tk.Entry(window)
name_entry.pack()

# Category
tk.Label(window, text="Select Category").pack()
category = ttk.Combobox(window, values=["Python", "HR", "AI"])
category.pack()

# Question
question_label = tk.Label(window, text="", wraplength=600, font=("Arial", 14))

# Answer Label
answer_label = tk.Label(window, text="Your Answer")

# Answer Box
answer_box = tk.Text(window, height=5, width=50)

# Result Label
result_label = tk.Label(window, text="", wraplength=600, font=("Arial", 12))


# Start Interview Function
def start_interview():
    global round_number, question_list, total_score

    selected_category = category.get()

    if selected_category:
        start_btn.config(state="disabled")
        round_number = 1
        total_score = 0

        question_list = questions[selected_category].copy()
        random.shuffle(question_list)

        round_label.config(text=f"Round: {round_number}/5")
        question_label.config(text="Question: " + question_list[0])
        result_label.config(text="")
        answer_box.delete("1.0", tk.END)


# Submit Answer Function
def submit_answer():
    global round_number, total_score

    answer = answer_box.get("1.0", tk.END).strip()

    question = question_list[round_number - 1]

    score, feedback = analyze_answer(question, answer)
    total_score += score

    result_text = f"Score: {score}/10\n"
    for item in feedback:
        result_text += item + "\n"

    result_label.config(text=result_text)

    answer_box.delete("1.0", tk.END)

    round_number += 1

    if round_number <= 5:
        round_label.config(text=f"Round: {round_number}/5")
        question_label.config(text="Question: " + question_list[round_number - 1])
        result_label.config(text="")

    else:
        avg = total_score / 5
        question_label.config(text="Interview Completed!")
        round_label.config(text=f"Final Score: {avg:.1f}/10")

        start_btn.pack_forget()
        submit_btn.pack_forget()
        answer_box.pack_forget()
        answer_label.pack_forget()
        result_label.config(text="")


# Restart Function
def restart():
    global round_number, total_score

    round_number = 0
    total_score = 0

    round_label.config(text="Round: 0/5")
    question_label.config(text="")
    result_label.config(text="")

    start_btn.config(state="normal") 
    answer_box.pack()
    start_btn.pack()
    submit_btn.pack()
    answer_label.pack()

    answer_box.delete("1.0", tk.END)

# Buttons
start_btn = tk.Button(window, text="Start Interview", command=start_interview)
submit_btn = tk.Button(window, text="Submit Answer", command=submit_answer)
restart_btn = tk.Button(window, text="Restart", command=restart)

# Pack in proper order
start_btn.pack(pady=10)
question_label.pack(pady=20)
answer_label.pack()
answer_box.pack()
submit_btn.pack(pady=10)
result_label.pack(pady=20)
restart_btn.pack(pady=10)

window.mainloop()