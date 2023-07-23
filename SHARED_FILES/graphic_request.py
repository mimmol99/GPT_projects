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

def select_item_from_list(item_list):
    # Create the root window
    root = tk.Tk()
    root.title('Select an item')
    
    # Create a StringVar() to store the selected item
    selected_item = tk.StringVar()

    # Create a Listbox widget
    listbox = tk.Listbox(root, exportselection=0, width=50,height=20)
    for item in item_list:
        listbox.insert(tk.END, item)
    listbox.pack()

    # Function to handle item selection
    def on_select(event):
        # Check if an item is selected
        if listbox.curselection():
            # Get selected item
            selection = event.widget.get(event.widget.curselection())
            selected_item.set(selection)
            # Show a message box with the selected item
            messagebox.showinfo("Selection", f"You selected: {selection}")
            # Close the window after selection
            root.withdraw()
            
            

    # Bind the select function to the listbox selection event
    listbox.bind('<<ListboxSelect>>', on_select)
    
    # Run the tkinter event loop
    root.mainloop()
    
    root.destroy()
    
    # Return the selected item
    return selected_item.get()