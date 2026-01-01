import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import random

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Adjust voice speed
engine.setProperty('volume', 1)  # Max volume

# Motivational responses
motivational_quotes = [
    "Believe in yourself! You are capable of amazing things.",
    "Your only limit is your mind. Keep pushing forward!",
    "Every challenge is an opportunity to grow stronger.",
    "Don't stop until you're proud of yourself.",
    "Mistakes are proof that you are trying. Keep going!",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "You are stronger than you think. Keep believing!"
]

# Function to respond with motivation
def motivate():
    user_text = entry.get().strip()
    if user_text:
        response = random.choice(motivational_quotes)  # Pick a random response
        chat_area.configure(state='normal')  # Enable editing
        chat_area.insert(tk.END, f"You: {user_text}\n", "user")
        chat_area.insert(tk.END, f"Coach: {response}\n\n", "coach")
        chat_area.configure(state='disabled')  # Disable editing
        chat_area.yview(tk.END)  # Auto-scroll
        
        entry.delete(0, tk.END)  # Clear input field
        
        # Speak response
        engine.say(response)
        engine.runAndWait()

# GUI Setup
root = tk.Tk()
root.title("AI Life Coach")
root.geometry("500x600")
root.resizable(True, True)
root.configure(bg="#EEC81D")

# Chat history area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black")
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.tag_config("user", foreground="blue", font=("Arial", 12, "bold"))
chat_area.tag_config("coach", foreground="green", font=("Arial", 12, "italic"))
chat_area.configure(state='disabled')  # Read-only mode

# Input field
entry = tk.Entry(root, font=("Arial", 14), bg="white", fg="black", bd=2)
entry.pack(padx=20, pady=5, fill=tk.X)
entry.bind("<Return>", lambda event: motivate())  # Press Enter to submit

# Send button
send_button = tk.Button(root, text="Motivate Me!", command=motivate, font=("Arial", 12), bg="#007BFF", fg="white", bd=2, relief="raised")
send_button.pack(pady=10)

# Run the application
root.mainloop()