import tkinter as tk
from tkinter import messagebox

class HumanVerificationInterface:
    def __init__(self, task_data):
        self.task_data = task_data
        self.root = tk.Tk()
        self.root.title("Human Verification Interface")

        # Task display
        tk.Label(self.root, text="Task:").pack()
        tk.Label(self.root, text=self.task_data['task_type']).pack()
        tk.Label(self.root, text=self.task_data['data']).pack()

        # Verification buttons
        tk.Button(self.root, text="Verify", command=self.verify_task).pack()
        tk.Button(self.root, text="Reject", command=self.reject_task).pack()

    def verify_task(self):
        # Send verification result to engine
        messagebox.showinfo("Task Verified", "Task verified successfully!")
        self.root.destroy()

    def reject_task(self):
        # Send rejection result to engine
        messagebox.showinfo("Task Rejected", "Task rejected!")
        self.root.destroy()

    def run(self):
        self.root.mainloop()
