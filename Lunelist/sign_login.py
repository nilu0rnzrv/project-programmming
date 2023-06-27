import tkinter as tk
import sqlite3
import subprocess
import os

def init_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL)''')

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()

    conn.close()

    return result is not None

def sign_up():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please enter both the username and password.")
        return

    if verify_user(username, password):
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Username already exists.                    Please choose a different username.")
    else:
        add_user(username, password)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Sign up successful!")

def log_in():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please enter both the username and password.")
        return

    if verify_user(username, password):
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Log in successful. Opening Lunelist...")
        window.withdraw()
        open_lunelist_app()
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid username or password.")

def open_lunelist_app():
    subprocess.run(["python", "lunelist.py"])
    window.destroy()

window = tk.Tk()
window.title("Lunelist")
window.geometry("320x430")

logo_path = "lunelist_logo.png"
if os.path.exists(logo_path):
    logo_image = tk.PhotoImage(file=logo_path)
    logo_label = tk.Label(window, image=logo_image)
    logo_label.pack(pady=5)

title_frame = tk.Frame(window)
title_frame.pack(pady=5)

title_label = tk.Label(title_frame, text="Lunelist", fg="#A24040", font=("Arial", 25, "bold"))
title_label.pack()

username_label = tk.Label(window, text="Username:")
username_label.pack()
title_frame = tk.Frame(window)
title_frame.pack(pady=5)

username_entry = tk.Entry(window)
username_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()

password_entry = tk.Entry(window, show="*")
password_entry.pack()

button_width = 6
sign_up_button = tk.Button(window,fg="#A24040", text="Sign Up", command=sign_up, width=button_width)
sign_up_button.pack(pady=5)

log_in_button = tk.Button(window, text="Log In", command=log_in, width=button_width)
log_in_button.pack(pady=5)

result_text = tk.Text(window, fg="#A24040", height=8, width=45)
result_text.pack()

init_database()

window.mainloop()
