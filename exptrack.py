import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# File to store expenses
FILE_NAME = "expenses.csv"

# Add Expense Function
def add_expense():
    amount = amount_entry.get()
    category = category_entry.get()
    description = description_entry.get()

    if amount == "" or category == "":
        messagebox.showerror("Error", "Amount and Category are required!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    expenses_tree.insert("", "end", values=(amount, category, description))
    save_expense(amount, category, description)

    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# Save expense to CSV
def save_expense(amount, category, description):
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([amount, category, description])

# Load expenses from CSV
def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                expenses_tree.insert("", "end", values=row)

# Main Window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x500")

# Input Fields
tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Category:").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Description:").pack()
description_entry = tk.Entry(root)
description_entry.pack()

tk.Button(root, text="Add Expense", command=add_expense).pack(pady=10)

# Expense Table
columns = ("Amount", "Category", "Description")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    expenses_tree.heading(col, text=col)
expenses_tree.pack(expand=True, fill="both")

load_expenses()

root.mainloop()