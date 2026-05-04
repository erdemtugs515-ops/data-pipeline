import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

#database
conn = sqlite3.connect("app.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,title TEXT,description TEXT,priority TEXT,status TEXT,due_date TEXT)""")
conn.commit()

#authentication thingy
def register():
    u = username_entry.get()
    p = password_entry.get()

    if not u or not p:
        messagebox.showwarning("Error", "Fill all fields")
        return
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
        conn.commit()
        messagebox.showinfo("Success", "Registered!")
    except:
        messagebox.showerror("Error", "Username exists")
def login():
    u = username_entry.get()
    p = password_entry.get()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    user = cursor.fetchone()
    if user:
        open_task_window(user[0])
    else:
        messagebox.showerror("Error", "Invalid login")

#task window
def open_task_window(user_id):
    win = Toplevel(root)
    win.title("Task Manager")
    win.geometry("700x500")

    #input section
    form = Frame(win)
    form.pack(pady=10)

    title_var = StringVar()
    desc_var = StringVar()
    priority_var = StringVar(value="Medium")
    status_var = StringVar(value="To Do")
    due_var = StringVar()
    Entry(form, textvariable=title_var, width=20).grid(row=0, column=0)
    Entry(form, textvariable=desc_var, width=20).grid(row=0, column=1)
    ttk.Combobox(form, textvariable=priority_var,
                 values=["Low", "Medium", "High"], width=10).grid(row=0, column=2)
    ttk.Combobox(form, textvariable=status_var,
                 values=["To Do", "In Progress", "Done"], width=12).grid(row=0, column=3)
    Entry(form, textvariable=due_var, width=12).grid(row=0, column=4)

    #task list
    frame = Frame(win)
    frame.pack(fill=BOTH, expand=True)
    canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    task_frame = Frame(canvas)
    task_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=task_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    #functions
    def load_tasks(filter_status="All"):
        for w in task_frame.winfo_children():
            w.destroy()
        query = "SELECT * FROM tasks WHERE user_id=?"
        params = [user_id]
        if filter_status != "All":
            query += " AND status=?"
            params.append(filter_status)
        cursor.execute(query, params)
        tasks = cursor.fetchall()
        for t in tasks:
            draw_task(t)

    def add_task():
        if not title_var.get():
            return

        # date validation
        if due_var.get():
            try:
                datetime.strptime(due_var.get(), "%Y-%m-%d")
            except:
                messagebox.showerror("Error", "Invalid date")
                return

        cursor.execute("""INSERT INTO tasks (user_id, title, description, priority, status, due_date)VALUES (?, ?, ?, ?, ?, ?)""", (user_id, title_var.get(), desc_var.get(),
              priority_var.get(), status_var.get(), due_var.get()))
        conn.commit()
        load_tasks()

    def delete_task(task_id):
        if messagebox.askyesno("Confirm", "Delete task?"):
            cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()
            load_tasks()

    def edit_task(task):
        edit_win = Toplevel(win)
        t_var = StringVar(value=task[2])
        d_var = StringVar(value=task[3])
        p_var = StringVar(value=task[4])
        s_var = StringVar(value=task[5])
        due_e = StringVar(value=task[6])
        Entry(edit_win, textvariable=t_var).pack()
        Entry(edit_win, textvariable=d_var).pack()
        ttk.Combobox(edit_win, textvariable=p_var,
                     values=["Low", "Medium", "High"]).pack()
        ttk.Combobox(edit_win, textvariable=s_var,
                     values=["To Do", "In Progress", "Done"]).pack()
        Entry(edit_win, textvariable=due_e).pack()

        def save():
            cursor.execute("""UPDATE tasks SET title=?, description=?, priority=?, status=?, due_date=?WHERE id=?""", (t_var.get(), d_var.get(), p_var.get(), s_var.get(), due_e.get(), task[0]))

            conn.commit()
            edit_win.destroy()
            load_tasks()

        Button(edit_win, text="Save", command=save).pack()

    def draw_task(task):
        card = Frame(task_frame, bd=1, relief="solid", padx=5, pady=5)
        card.pack(fill=X, pady=4)
        Label(card, text=f"{task[2]} ({task[4]} | {task[5]})").pack(anchor="w")
        Label(card, text=task[3]).pack(anchor="w")
        due = task[6] if task[6] else "No due date"
        Label(card, text=f"Due: {due}").pack(anchor="w")
        Button(card, text="Edit", command=lambda: edit_task(task)).pack(side=RIGHT)
        Button(card, text="Delete", command=lambda: delete_task(task[0])).pack(side=RIGHT)

    #filter for tasks
    filter_var = StringVar(value="All")
    ttk.Combobox(win, textvariable=filter_var,
                 values=["All", "To Do", "In Progress", "Done"]).pack()
    Button(win, text="Apply Filter",
           command=lambda: load_tasks(filter_var.get())).pack()
    Button(form, text="Add Task", command=add_task).grid(row=0, column=5)
    load_tasks()


#main UI
root = Tk()
root.title("Login")
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Username").grid(column=0, row=0)
ttk.Label(frm, text="Password").grid(column=0, row=1)
username_entry = ttk.Entry(frm)
password_entry = ttk.Entry(frm, show="*")
username_entry.grid(column=1, row=0)
password_entry.grid(column=1, row=1)
ttk.Button(frm, text="Login", command=login).grid(column=1, row=2)
ttk.Button(frm, text="Register", command=register).grid(column=2, row=2)
root.mainloop()