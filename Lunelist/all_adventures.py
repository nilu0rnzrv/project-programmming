import tkinter as tk
import sqlite3
import webbrowser
import subprocess

def load_adventures():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute("SELECT task, points FROM tasks")
    result = c.fetchall()
    conn.close()
    return result

def collect_adventure(points, adventure_frame):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute("INSERT INTO collected_points (points) VALUES (?)", (points,))
    conn.commit()
    conn.close()

    adventure_frame.pack_forget()  # Remove the adventure frame from the GUI

    calculate_total_points()

def update_total_points(points):
    total_points_label.config(text=f"🥳 Total Points: {points}")

def calculate_total_points():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute("SELECT SUM(points) FROM collected_points")
    result = c.fetchone()
    total_points = result[0] if result[0] else 0

    conn.close()

    update_total_points(total_points)

def share_via_whatsapp(points):
    message = f"Hey! I've collected {points} points in adventures. 🥳"
    webbrowser.open(f"https://web.whatsapp.com/send?text={message}")

def share_via_telegram(points):
    message = f"Hey! I've collected {points} points in adventures. 🥳"
    webbrowser.open(f"https://telegram.me/share?url=&text={message}")

def share_via_instagram(points):
    message = f"Hey! I've collected {points} points in adventures. 🥳"
    webbrowser.open(f"https://www.instagram.com/?message={message}")

def share_options(points):
    menu = tk.Menu(window, tearoff=0)
    menu.add_command(label="WhatsApp", command=lambda: share_via_whatsapp(points))
    menu.add_command(label="Telegram", command=lambda: share_via_telegram(points))
    menu.add_command(label="Instagram", command=lambda: share_via_instagram(points))
    menu.tk_popup(window.winfo_pointerx(), window.winfo_pointery())

def back_to_lunelist():
    window.destroy()
    subprocess.run(['python', 'lunelist.py'])

window = tk.Tk()
window.title("Adventure List")
window.geometry("320x600")
logo_path = "lunelist_logo.png"
logo_image = tk.PhotoImage(file=logo_path)
logo_label = tk.Label(window, image=logo_image)
logo_label.image = logo_image
logo_label.pack(pady=10)

total_points_label = tk.Label(window, text="🥳 Total Points: 0", fg="#A24040", font=("Arial", 16, "bold"))
total_points_label.pack()

list_frame = tk.Frame(window)
list_frame.pack(pady=10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

adventure_list = tk.Text(list_frame, width=30, height=10, yscrollcommand=scrollbar.set)
adventure_list.pack(side=tk.LEFT)

scrollbar.config(command=adventure_list.yview)

def populate_adventures():
    adventures = load_adventures()

    for adventure in adventures:
        task, points = adventure

        adventure_frame = tk.Frame(adventure_list)
        adventure_frame.pack(pady=3)

        task_label = tk.Label(adventure_frame, text=task, width=25, anchor="w")
        task_label.pack(side=tk.LEFT, padx=(1, 0))

        points_label = tk.Label(adventure_frame, fg="#A24040", text=points)
        points_label.pack(side=tk.LEFT)

        done_button = tk.Button(adventure_frame, text="Done", command=lambda p=points, af=adventure_frame: collect_adventure(p, af))
        done_button.pack(side=tk.LEFT, padx=1)

        adventure_frame.adventure_frame = adventure_frame

populate_adventures()

def open_maps():
    map_url = "https://www.google.com/maps/search/places+to+visit+in+l%C3%BCneburg/@53.2518053,10.3847111,14z/data=!3m1!4b1?entry=ttu"
    webbrowser.open(map_url)

buttons_frame = tk.Frame(window)
buttons_frame.pack(side=tk.BOTTOM, pady=10)

back_button = tk.Button(buttons_frame, text="Back", fg="black", command=back_to_lunelist)
back_button.pack(side=tk.LEFT)

maps_button = tk.Button(buttons_frame, text="Maps", command=open_maps)
maps_button.pack(side=tk.LEFT, padx=10)

share_button = tk.Button(buttons_frame, text="Share", fg="#A24040", font=("Arial", 13, "bold"), command=lambda: share_options(sum(collected_points)))
share_button.pack(side=tk.RIGHT)

window.mainloop()
