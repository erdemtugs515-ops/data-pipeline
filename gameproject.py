import sqlite3
from tkinter import*
from tkinter import ttk

#database junk
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)""")

conn.commit()

#register function
def register():
    username = username_entry.get()
    password = password_entry.get()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    print("User registered")

#login func
def login():
    username = username_entry.get()
    password = password_entry.get()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    if result:
        print("Login successful")
    else:
        print("Invalid credentials")

#showing users for testing
def show_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)


#UI section? (please work)
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Login").grid(column=1, row=0)
ttk.Label(frm, text="Username").grid(column=0, row=1)
ttk.Label(frm, text="Password").grid(column=0, row=2)
username_entry = ttk.Entry(frm)
password_entry = ttk.Entry(frm)
username_entry.grid(column=1, row=1)
password_entry.grid(column=1, row=2)
ttk.Button(frm, text="Login", command=login).grid(column=1, row=3)
ttk.Button(frm, text="Register", command=register).grid(column=2, row=3)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=3, row=5)
root.mainloop()



#https://miraavorne.github.io/Python_game/projekti.html
#study what sql injetion is, how to prevent it and how to do it