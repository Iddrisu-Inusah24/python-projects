import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import os
from collections import defaultdict

# Matplotlib for charts (no pyplot needed)
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

APP_TITLE = "Expense Tracker Pro"
FILE_NAME = "expenses.csv"
EXPECTED_HEADERS = ["date", "amount", "category", "description"]

# ---------------------------- THEME SETUP ---------------------------- #
# Define themes
LIGHT_MODE = {
    "BG": "#ECF0F1",
    "FG": "black",
    "INPUT_BG": "white",
    "BTN_BG": "#BDC3C7",
    "BTN_ACTIVE": "#95A5A6",
    "TREE_BG": "white",
    "TREE_FG": "black",
    "TREE_SEL_BG": "#D6DBDF",
    "TREE_SEL_FG": "black"
}

DARK_MODE = {
    "BG": "#2C3E50",
    "FG": "white",
    "INPUT_BG": "#ECF0F1",
    "BTN_BG": "#34495E",
    "BTN_ACTIVE": "#1ABC9C",
    "TREE_BG": "#263445",
    "TREE_FG": "white",
    "TREE_SEL_BG": "#1ABC9C",
    "TREE_SEL_FG": "black"
}

# Combine themes in a dictionary
THEMES = {
    "light": LIGHT_MODE,
    "dark": DARK_MODE
}

# Default theme
current_theme = "light"
theme = THEMES[current_theme].copy()


def set_theme(style: ttk.Style):
    """Apply theme colors to the whole UI."""
    root.configure(bg=theme["BG"])

    # ttk styles (for ttk widgets only)
    style.configure("TLabel", background=theme["BG"], foreground=theme["FG"])
    style.configure("TButton", background=theme["BTN_BG"], foreground=theme["FG"])
    style.map("TButton",
              background=[("active", theme["BTN_ACTIVE"])],
              foreground=[("active", theme["FG"])])

    style.configure("Treeview",
                    background=theme["TREE_BG"],
                    foreground=theme["TREE_FG"],
                    fieldbackground=theme["TREE_BG"])
    style.map("Treeview",
              background=[("selected", theme["TREE_SEL_BG"])],
              foreground=[("selected", theme["TREE_SEL_FG"])])

    style.configure("TEntry", fieldbackground=theme["INPUT_BG"], foreground=theme["FG"])
    style.configure("TCombobox", fieldbackground=theme["INPUT_BG"], foreground=theme["FG"])

    # Recursively theme classic tk widgets only
    for widget in root.winfo_children():
        apply_widget_theme(widget)

def apply_widget_theme(widget):
    theme = THEMES[current_theme]
    try:
        if isinstance(widget, (tk.Entry, tk.Text)):
            widget.configure(bg=theme["INPUT_BG"], fg=theme["FG"], insertbackground=theme["FG"])
        elif isinstance(widget, (tk.Label, tk.Button, tk.Frame)):
            widget.configure(bg=theme["BG"], fg=theme["FG"])
    except tk.TclError:
        pass  # Skip widgets that do not support these options

    # Recursively apply theme to child widgets
    for child in widget.winfo_children():
        apply_widget_theme(child)

def toggle_theme():
    """Switch between light and dark theme."""
    global theme
    theme = DARK_MODE.copy() if theme == LIGHT_MODE else LIGHT_MODE.copy()
    set_theme(style)

# ---------------------------- DATA LAYER ---------------------------- #
def ensure_file():
    """Create CSV with correct headers if it doesn't exist or is malformed."""
    needs_rewrite = False
    if not os.path.exists(FILE_NAME):
        needs_rewrite = True
    else:
        # Verify header row
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if not first_line or [h.strip() for h in first_line.split(",")] != EXPECTED_HEADERS:
                needs_rewrite = True

    if needs_rewrite:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(EXPECTED_HEADERS)

def load_expenses_into_tree():
    """Load CSV rows into the Treeview, skipping malformed rows."""
    expenses_tree.delete(*expenses_tree.get_children())
    ensure_file()

    with open(FILE_NAME, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        # If headers are wrong, repair file and show empty table
        if reader.fieldnames != EXPECTED_HEADERS:
            with open(FILE_NAME, "w", newline="", encoding="utf-8") as fw:
                csv.writer(fw).writerow(EXPECTED_HEADERS)
            update_summary()
            return

        for row in reader:
            # Guard against missing keys or bad numbers
            try:
                date = row.get("date", "").strip()
                amount = float(row.get("amount", "0").strip() or "0")
                category = row.get("category", "").strip()
                desc = row.get("description", "").strip()
                if not date or not category:
                    continue
                expenses_tree.insert("", "end", values=(date, f"{amount:.2f}", category, desc))
            except Exception:
                # Skip malformed rows
                continue

    update_summary()

def append_expense_to_file(date_str, amount, category, desc):
    """Append a single expense to the CSV file."""
    ensure_file()
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, f"{amount:.2f}", category, desc])

def rewrite_file_from_tree():
    """Rewrite the CSV file from all rows in the Treeview (used after deletion)."""
    ensure_file()
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(EXPECTED_HEADERS)
        for item in expenses_tree.get_children():
            writer.writerow(expenses_tree.item(item, "values"))

# ---------------------------- BUSINESS LOGIC ---------------------------- #
def add_expense():
    date_str = date_entry.get().strip()
    amount_str = amount_entry.get().strip()
    category = category_var.get().strip()
    desc = desc_entry.get().strip()

    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # Validate date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date", "Use date format YYYY-MM-DD.")
        return

    # Validate amount
    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("Invalid Amount", "Amount must be a number.")
        return

    if not category:
        messagebox.showerror("Missing Category", "Please enter or select a category.")
        return

    # Insert into Treeview
    expenses_tree.insert("", "end", values=(date_str, f"{amount:.2f}", category, desc))

    # Append to file
    append_expense_to_file(date_str, amount, category, desc)

    # Clear inputs
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

    update_summary()

def delete_selected():
    selected = expenses_tree.selection()
    if not selected:
        messagebox.showinfo("Delete", "Please select one or more rows to delete.")
        return

    if messagebox.askyesno("Confirm Delete", f"Delete {len(selected)} selected item(s)?"):
        for item in selected:
            expenses_tree.delete(item)
        rewrite_file_from_tree()
        update_summary()

def update_summary():
    """Compute total amount and totals per category; update labels."""
    total = 0.0
    count = 0
    cat_totals = defaultdict(float)

    for item in expenses_tree.get_children():
        _, amount_str, category, _ = expenses_tree.item(item, "values")
        try:
            amt = float(amount_str)
        except ValueError:
            amt = 0.0
        total += amt
        count += 1
        cat_totals[category] += amt

    total_label_var.set(f"Total Spent: {total:.2f}   |   Items: {count}")
    if cat_totals:
        top_cat = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)[:3]
        cats_text = "   •   ".join([f"{k}: {v:.2f}" for k, v in top_cat])
    else:
        cats_text = "No expenses yet."
    category_summary_var.set(f"Top Categories: {cats_text}")

def show_pie_chart():
    """Display a pie chart of category totals in a new window."""
    cat_totals = defaultdict(float)
    for item in expenses_tree.get_children():
        _, amount_str, category, _ = expenses_tree.item(item, "values")
        try:
            amt = float(amount_str)
        except ValueError:
            amt = 0.0
        cat_totals[category] += amt

    if not cat_totals:
        messagebox.showinfo("Chart", "No data to plot yet.")
        return

    # New window for the chart
    chart_win = tk.Toplevel(root)
    chart_win.title("Expenses by Category")
    chart_win.configure(bg=theme["BG"])

    # Build the Matplotlib Figure (single chart, defaults for colors)
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    labels = list(cat_totals.keys())
    sizes = list(cat_totals.values())

    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Equal aspect ratio for a circle

    canvas = FigureCanvasTkAgg(fig, master=chart_win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def export_as_csv():
    """Let user choose a location to export the current table as CSV."""
    path = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV files", "*.csv")],
                                        initialfile="expenses_export.csv",
                                        title="Export Expenses")
    if not path:
        return

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(EXPECTED_HEADERS)
        for item in expenses_tree.get_children():
            writer.writerow(expenses_tree.item(item, "values"))

    messagebox.showinfo("Export", f"Exported to:\n{path}")

# ---------------------------- UI SETUP ---------------------------- #
root = tk.Tk()
root.title(APP_TITLE)
root.geometry("820x620")
root.minsize(760, 540)

style = ttk.Style()
# Use a theme that allows Treeview styling cross-platform
try:
    style.theme_use("clam")
except tk.TclError:
    pass

# Top Title + Theme Toggle
title_frame = tk.Frame(root)
title_frame.pack(fill="x", pady=(10, 0), padx=10)

title_label = ttk.Label(title_frame, text="Expense Tracker Pro", font=("Arial", 18, "bold"))
title_label.pack(side="left")

theme_btn = tk.Button(title_frame, text="Toggle Theme", command=toggle_theme)
theme_btn.pack(side="right")

# Input Section
input_frame = tk.LabelFrame(root, text="Add Expense", padx=10, pady=10)
input_frame.pack(fill="x", padx=10, pady=10)

# Date
ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=4)
date_entry = tk.Entry(input_frame)
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
date_entry.grid(row=0, column=1, sticky="ew", pady=4)

# Amount
ttk.Label(input_frame, text="Amount:").grid(row=0, column=2, sticky="w", padx=(12, 6), pady=4)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=0, column=3, sticky="ew", pady=4)

# Category (Combobox + allow free text)
ttk.Label(input_frame, text="Category:").grid(row=1, column=0, sticky="w", padx=(0, 6), pady=4)
category_var = tk.StringVar()
category_entry = ttk.Combobox(input_frame, textvariable=category_var)
category_entry["values"] = ["Food", "Transport", "Bills", "Education", "Health", "Clothing", "Entertainment", "Other"]
category_entry.grid(row=1, column=1, sticky="ew", pady=4)

# Description
ttk.Label(input_frame, text="Description:").grid(row=1, column=2, sticky="w", padx=(12, 6), pady=4)
desc_entry = tk.Entry(input_frame)
desc_entry.grid(row=1, column=3, sticky="ew", pady=4)

# Buttons
btn_frame = tk.Frame(input_frame)
btn_frame.grid(row=0, column=4, rowspan=2, padx=(12, 0), sticky="ns")

add_btn = tk.Button(btn_frame, text="Add", width=12, command=add_expense)
add_btn.pack(pady=(0, 6), fill="x")

del_btn = tk.Button(btn_frame, text="Delete Selected", width=12, command=delete_selected)
del_btn.pack(pady=(0, 6), fill="x")

chart_btn = tk.Button(btn_frame, text="Pie Chart", width=12, command=show_pie_chart)
chart_btn.pack(pady=(0, 6), fill="x")

export_btn = tk.Button(btn_frame, text="Export CSV", width=12, command=export_as_csv)
export_btn.pack(fill="x")

# Grid weights for input_frame
input_frame.columnconfigure(1, weight=1)
input_frame.columnconfigure(3, weight=1)

# Table Section
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

columns = ("date", "amount", "category", "description")
expenses_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
for col, text in zip(columns, ["Date", "Amount", "Category", "Description"]):
    expenses_tree.heading(col, text=text)
    # Set column widths
    if col == "description":
        expenses_tree.column(col, width=280, anchor="w")
    elif col == "amount":
        expenses_tree.column(col, width=100, anchor="e")
    else:
        expenses_tree.column(col, width=130, anchor="center")

# Scrollbars
ysb = ttk.Scrollbar(table_frame, orient="vertical", command=expenses_tree.yview)
xsb = ttk.Scrollbar(table_frame, orient="horizontal", command=expenses_tree.xview)
expenses_tree.configure(yscroll=ysb.set, xscroll=xsb.set)

expenses_tree.grid(row=0, column=0, sticky="nsew")
ysb.grid(row=0, column=1, sticky="ns")
xsb.grid(row=1, column=0, sticky="ew")

table_frame.columnconfigure(0, weight=1)
table_frame.rowconfigure(0, weight=1)

# Summary Section
summary_frame = tk.Frame(root)
summary_frame.pack(fill="x", padx=10, pady=(0, 12))

total_label_var = tk.StringVar(value="Total Spent: 0.00   |   Items: 0")
category_summary_var = tk.StringVar(value="Top Categories: -")

total_label = ttk.Label(summary_frame, textvariable=total_label_var, font=("Arial", 12, "bold"))
total_label.pack(side="left")

category_label = ttk.Label(summary_frame, textvariable=category_summary_var)
category_label.pack(side="right")

# Initialize
set_theme(style)
ensure_file()
load_expenses_into_tree()

# Run
if __name__ == "__main__":
    root.mainloop()