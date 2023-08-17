import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def request_file_path(title=None):
    # Create a root window
    root = tk.Tk()

    # Hide the root window
    root.withdraw()

    # Ask the user to select a directory
    file_path = filedialog.askopenfilename(title = title)

    # Print the selected directory
    return file_path
    
def request_file_paths(title=None):
    # Create a root window
    root = tk.Tk()

    # Hide the root window
    root.withdraw()

    # Ask the user to select a directory
    file_paths = filedialog.askopenfilenames(title = title)

    # Print the selected directory
    return file_paths
    
def request_folder_path(title=None):
    # Create a root window
    root = tk.Tk()

    # Hide the root window
    root.withdraw()

    # Ask the user to select a folder
    folder_path = filedialog.askdirectory(title=title)

    # Print the selected folder
    return folder_path

def request_string(title=None):
    # Create a root window
    root = tk.Tk()

    # Hide the root window
    root.withdraw()

    # Ask the user to enter a string
    string = tk.simpledialog.askstring(title=title, prompt="Enter a string:")

    # Print the entered string
    return string


