import tkinter as tk
from tkinter import simpledialog

def request_input(title="Input", prompt="Please enter input:", default_value=""):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    user_input = simpledialog.askstring(title, prompt, initialvalue=default_value)
    return user_input
