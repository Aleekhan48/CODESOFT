import tkinter as tk
from tkinter import messagebox
import json

TODO_FILE = "todo_list.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        self.todo_list = self.load_todo_list()

        self.task_var = tk.StringVar()
        self.task_entry = tk.Entry(root, textvariable=self.task_var, width=30)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=10, pady=10)

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=40, height=10)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.display_tasks()

        self.mark_completed_button = tk.Button(root, text="Mark Completed", command=self.mark_completed)
        self.mark_completed_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_todo_list(self):
        try:
            with open(TODO_FILE, "r") as file:
                todo_list = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            todo_list = []
        return todo_list

    def save_todo_list(self):
        with open(TODO_FILE, "w") as file:
            json.dump(self.todo_list, file)

    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.todo_list:
            status = "[ ]" if not task["completed"] else "[X]"
            self.task_listbox.insert(tk.END, f"{status} {task['title']}")

    def add_task(self):
        title = self.task_var.get()
        if title:
            task = {"title": title, "completed": False}
            self.todo_list.append(task)
            self.save_todo_list()
            self.display_tasks()
            self.task_var.set("")
        else:
            messagebox.showwarning("Warning", "Please enter a task title.")

    def mark_completed(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.todo_list[index]["completed"] = True
            self.save_todo_list()
            self.display_tasks()

    def on_close(self):
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
