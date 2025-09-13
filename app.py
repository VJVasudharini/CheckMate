import tkinter as tk
from tkinter import messagebox
from todo_db import init_db, add_task, list_tasks, mark_done, delete_task

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CheckMate - Todo List Manager")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        init_db()

        # --- Entry Field ---
        self.task_entry = tk.Entry(root, font=("Arial", 14))
        self.task_entry.pack(pady=10, padx=10, fill=tk.X)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        # --- Listbox ---
        self.task_listbox = tk.Listbox(root, font=("Arial", 12), selectmode=tk.SINGLE)
        self.task_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # --- Buttons ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.done_button = tk.Button(btn_frame, text="Mark Done", command=self.mark_done)
        self.done_button.grid(row=0, column=0, padx=5)

        self.undo_button = tk.Button(btn_frame, text="Undo", command=self.undo_done)
        self.undo_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(btn_frame, text="Delete", command=self.delete_task)
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
