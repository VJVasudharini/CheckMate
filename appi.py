import tkinter as tk
from tkinter import messagebox
from todo_db import init_db, add_task, list_tasks, mark_done, delete_task

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CheckMate - Todo List Manager")
        self.root.geometry("450x550")
        self.root.configure(bg="#f4f6f7")
        self.root.resizable(False, False)

        init_db()

        # --- Title ---
        title_label = tk.Label(
            root, text="📝 CheckMate - Todo List Manager", font=("Arial", 20, "bold"), bg="#f4f6f7", fg="#2c3e50"
        )
        title_label.pack(pady=10)

        # --- Entry Section ---
        entry_frame = tk.Frame(root, bg="#f4f6f7")
        entry_frame.pack(pady=10, padx=10, fill=tk.X)

        entry_label = tk.Label(
            entry_frame, text="Enter a Task:", font=("Arial", 12, "bold"), bg="#f4f6f7", fg="#34495e"
        )
        entry_label.pack(anchor="w")

        self.task_entry = tk.Entry(entry_frame, font=("Arial", 14))
        self.task_entry.pack(fill=tk.X, pady=5)

        self.add_button = tk.Button(
            entry_frame, text="Add Task", font=("Arial", 12, "bold"),
            bg="#27ae60", fg="white", command=self.add_task
        )
        self.add_button.pack(pady=5, fill=tk.X)

        # --- Listbox Section ---
        self.task_listbox = tk.Listbox(
            root, font=("Arial", 12), selectmode=tk.SINGLE,
            bg="#ecf0f1", fg="#2c3e50", activestyle="none"
        )
        self.task_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # --- Buttons Section ---
        btn_frame = tk.Frame(root, bg="#f4f6f7")
        btn_frame.pack(pady=10)

        self.done_button = tk.Button(
            btn_frame, text="✔ Mark Done", font=("Arial", 11),
            bg="#2ecc71", fg="white", command=self.mark_done, width=12
        )
        self.done_button.grid(row=0, column=0, padx=5)

        self.undo_button = tk.Button(
            btn_frame, text="↩ Undo", font=("Arial", 11),
            bg="#f39c12", fg="white", command=self.undo_done, width=12
        )
        self.undo_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(
            btn_frame, text="🗑 Delete", font=("Arial", 11),
            bg="#e74c3c", fg="white", command=self.delete_task, width=12
        )
        self.delete_button.grid(row=0, column=2, padx=5)

        # Load tasks at startup
        self.refresh_tasks()

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.tasks = list_tasks()
        for task in self.tasks:
            tid, title, done = task
            status = "✔️" if done else "❌"
            self.task_listbox.insert(tk.END, f"{tid}. {title} [{status}]")

    def add_task(self):
        title = self.task_entry.get().strip()
        if title:
            add_task(title)
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks()
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!")

    def get_selected_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            return self.tasks[index]
        except IndexError:
            messagebox.showwarning("Selection Error", "No task selected!")
            return None

    def mark_done(self):
        task = self.get_selected_task()
        if task:
            mark_done(task[0], True)
            self.refresh_tasks()

    def undo_done(self):
        task = self.get_selected_task()
        if task:
            mark_done(task[0], False)
            self.refresh_tasks()

    def delete_task(self):
        task = self.get_selected_task()
        if task:
            delete_task(task[0])
            self.refresh_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
