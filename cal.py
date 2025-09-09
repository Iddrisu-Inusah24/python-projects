import tkinter as tk
from tkinter import messagebox
import math

# Color Themes
LIGHT_MODE = {
    "BG_COLOR": "#ECF0F1",
    "BTN_COLOR": "#BDC3C7",
    "BTN_HOVER": "#95A5A6",
    "TEXT_COLOR": "black",
    "ENTRY_BG": "white"
}

DARK_MODE = {
    "BG_COLOR": "#2C3E50",
    "BTN_COLOR": "#34495E",
    "BTN_HOVER": "#1ABC9C",
    "TEXT_COLOR": "white",
    "ENTRY_BG": "#300C58"
}

theme = LIGHT_MODE  # Default theme

def apply_theme():
    """Switch themes between Light and Dark mode"""
    global theme
    theme = DARK_MODE if theme == LIGHT_MODE else LIGHT_MODE
    root.config(bg=theme["BG_COLOR"])
    entry.config(bg=theme["ENTRY_BG"], fg=theme["TEXT_COLOR"])
    for btn in buttons_list:
        btn.config(bg=theme["BTN_COLOR"], fg=theme["TEXT_COLOR"], activebackground=theme["BTN_HOVER"])

def click(button_text):
    """Handles button clicks"""
    if button_text == "=":
        calculate()
    elif button_text == "C":
        clear()
    elif button_text == "⌫":
        backspace()
    elif button_text == "√":
        handle_sqrt()
    elif button_text == "^":
        entry_var.set(entry_var.get() + "**")
    elif button_text == "%":
        handle_percentage()
    elif button_text in ["sin", "cos", "tan", "log", "!"]:
        apply_scientific_function(button_text)
    else:
        entry_var.set(entry_var.get() + button_text)

def clear():
    """Clears the input field"""
    entry_var.set("")

def backspace():
    """Deletes the last character"""
    entry_var.set(entry_var.get()[:-1])

def handle_sqrt():
    """Handles square root operation"""
    try:
        result = math.sqrt(float(entry_var.get()))
        entry_var.set(str(result))
    except:
        entry_var.set("Error")

def handle_percentage():
    """Handles percentage calculation"""
    try:
        result = float(entry_var.get()) / 100
        entry_var.set(str(result))
    except:
        entry_var.set("Error")

def calculate():
    """Evaluates the expression"""
    try:
        result = eval(entry_var.get())
        entry_var.set(str(result))
    except:
        entry_var.set("Error")

def apply_scientific_function(func):
    """Applies scientific functions"""
    try:
        value = float(entry_var.get())
        if func == "sin":
            result = math.sin(math.radians(value))
        elif func == "cos":
            result = math.cos(math.radians(value))
        elif func == "tan":
            result = math.tan(math.radians(value))
        elif func == "log":
            result = math.log10(value)
        elif func == "!":
            result = math.factorial(int(value))
        entry_var.set(str(result))
    except:
        entry_var.set("Error")

# Main Window
root = tk.Tk()
root.title("Iddrisu Calculator")
root.geometry("380x600")
root.configure(bg=theme["BG_COLOR"])
root.resizable(True, True)  # Prevent window resizing

# Entry Field
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 22), justify="right", bg=theme["ENTRY_BG"], fg=theme["TEXT_COLOR"], bd=10, relief="ridge")
entry.pack(pady=10, padx=10, fill="x", ipady=10)

# Button Frame
button_frame = tk.Frame(root, bg=theme["BG_COLOR"])
button_frame.pack(expand=True, fill="both")

# Buttons Layout
buttons = [
    ('C', '⌫', '%', '/'),
    ('7', '8', '9', '*'),
    ('4', '5', '6', '-'),
    ('1', '2', '3', '+'),
    ('√', '0', '^', '='),
    ('sin', 'cos', 'tan', 'log'),
    ('!', '.', ',','※', )
]

buttons_list = []

# Generate Buttons
for row, values in enumerate(buttons):
    for col, text in enumerate(values):
        btn = tk.Button(
            button_frame, text=text, font=("Arial", 16), bg=theme["BTN_COLOR"], fg=theme["TEXT_COLOR"],
            activebackground=theme["BTN_HOVER"], relief="flat", width=6, height=2,
            command=lambda x=text: apply_theme() if x == "※" else click(x)
        )
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        buttons_list.append(btn)

# Adjust Grid
for i in range(4):
    button_frame.columnconfigure(i, weight=1)
for i in range(len(buttons)):
    button_frame.rowconfigure(i, weight=1)

# Run Application
root.mainloop()