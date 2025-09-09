import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from datetime import datetime

# Main App Window
root = tk.Tk()
root.title("Professional Attendance Register")
root.geometry("700x500")
root.resizable(False, False)

# Data Storage
attendance_data = []
serial_no = 1

# --- Functions ---
def add_student():
    global serial_no
    fname = first_name_entry.get().strip()
    lname = last_name_entry.get().strip()

    if fname == "" or lname == "":
        messagebox.showerror("Input Error", "First Name and Last Name are required!")
        return

    date_today = datetime.now().strftime("%Y-%m-%d")
    attendance_data.append([serial_no, fname, lname, date_today, "Absent"])
    
    tree.insert("", "end", values=(serial_no, fname, lname, date_today, "Absent"))
    serial_no += 1
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)

def toggle_attendance(event):
    selected_item = tree.selection()
    if selected_item:
        current_values = list(tree.item(selected_item, "values"))
        if current_values[4] == "Absent":
            current_values[4] = "Present"
        else:
            current_values[4] = "Absent"
        
        # Update in Treeview
        tree.item(selected_item, values=current_values)

        # Update in Data List
        for data in attendance_data:
            if data[0] == int(current_values[0]):  # Match Serial No
                data[4] = current_values[4]
                break

def export_csv():
    if not attendance_data:
        messagebox.showerror("Error", "No data to export!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Serial No", "First Name", "Last Name", "Date", "Attendance"])
            writer.writerows(attendance_data)
        messagebox.showinfo("Success", f"Attendance exported to {file_path}")

# --- UI Layout ---
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="First Name:").grid(row=0, column=0, padx=5)
first_name_entry = tk.Entry(frame_top)
first_name_entry.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="Last Name:").grid(row=0, column=2, padx=5)
last_name_entry = tk.Entry(frame_top)
last_name_entry.grid(row=0, column=3, padx=5)

add_btn = tk.Button(frame_top, text="Add Student", command=add_student)
add_btn.grid(row=0, column=4, padx=5)

# Treeview for Attendance Table
columns = ("Serial No", "First Name", "Last Name", "Date", "Attendance")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
tree.pack(fill="both", expand=True, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.bind("<Double-1>", toggle_attendance)

# Export Button
export_btn = tk.Button(root, text="Export to CSV", command=export_csv)
export_btn.pack(pady=10)

root.mainloop()