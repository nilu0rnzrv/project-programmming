import os
import pandas as pd
import tkinter as tk
import sqlite3
import subprocess

def init_database():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task TEXT NOT NULL,
                  points INTEGER NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS collected_points
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  points INTEGER NOT NULL)''')

    conn.commit()
    conn.close()

def add_task_to_database(n_task, points):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute("INSERT INTO tasks (task, points) VALUES (?, ?)", (n_task, points))

    conn.commit()
    conn.close()

def get_task_from_database(n_task, points):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute("SELECT * FROM tasks WHERE task=? AND points=?", (n_task, points))
    result = c.fetchone()

    conn.close()

    return result is not None

def load_tasks_from_database():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute("SELECT task, points FROM tasks")
    result = c.fetchall()

    conn.close()

    if result:
        tasks_df = pd.DataFrame(result, columns=['Task', 'Points'])
        return tasks_df.to_string(index=False)
    else:
        return "No tasks found in the database."

window = tk.Tk()
window.title("Lunelist")
window.geometry("320x500")

def add_task():
    n_task = task_entry.get()
    points = points_entry.get()

    if n_task == "" or points == "":
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please enter both the task and points.")
        return

    if get_task_from_database(n_task, points):
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "The task already exists in the list.")
    else:
        add_task_to_database(n_task, points)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Los geht's and have great time in Lüneburg!")

    task_entry.delete(0, tk.END)
    points_entry.delete(0, tk.END)

def view_all_tasks():
    window.destroy()
    subprocess.run(['python', 'all_adventures.py'])

def about_app():
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END,
                       "Lunelist helps international students get to know Lüneburg better + have unforgettable    experience.")

def terms_of_use():
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "I solemnly swear that I am up to no good!")

logo_path = "lunelist_logo.png"
if os.path.exists(logo_path):
    logo_image = tk.PhotoImage(file=logo_path)
    logo_label = tk.Label(window, image=logo_image)
    logo_label.pack(pady=10)

title_frame = tk.Frame(window)
title_frame.pack(pady=10)

title_label = tk.Label(title_frame, text="Welcome to Lunelist!", fg="#A24040", font=("Arial", 20, "bold"))
title_label.pack()

menu_frame = tk.Frame(window)
menu_frame.pack(pady=5)

button_width = 20

task_label = tk.Label(menu_frame, text="Enter Task:")
task_label.grid(row=0, column=0, pady=5)

task_entry = tk.Entry(menu_frame)
task_entry.grid(row=0, column=1, pady=5)

points_label = tk.Label(menu_frame, text="Enter Points:")
points_label.grid(row=1, column=0, pady=5)

points_entry = tk.Entry(menu_frame)
points_entry.grid(row=1, column=1, pady=5)

add_button = tk.Button(menu_frame, text="Add an Adventure", command=add_task, width=button_width)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

all_button = tk.Button(menu_frame, text="All Adventures", command=view_all_tasks, width=button_width)
all_button.grid(row=4, column=0, columnspan=2, pady=5)

about_button = tk.Button(menu_frame, text="About the App", command=about_app, width=button_width)
about_button.grid(row=6, column=0, columnspan=2, pady=5)

terms_button = tk.Button(menu_frame, text="Terms of Use and Policy", command=terms_of_use, width=button_width)
terms_button.grid(row=7, column=0, columnspan=2, pady=5)

result_text = tk.Text(window, fg="#A24040", height=10, width=45)
result_text.pack()

init_database()

window.mainloop()
