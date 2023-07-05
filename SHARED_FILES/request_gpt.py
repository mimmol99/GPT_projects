import openai
import tkinter as tk
from tkinter import  simpledialog,messagebox
import requests
import os
import tiktoken
import math

base_path = os.getcwd()
model_path = os.path.join(base_path,"model.txt")
openaiapi_path = os.path.join(base_path,"openaiapi.txt")

from SHARED_FILES.request_input import request_input
from SHARED_FILES.rate_limit import find_model_tokens_limit

def copy_to_clipboard(root, text):
    # Clear the clipboard
    root.clipboard_clear()
    # Copy the text to the clipboard
    root.clipboard_append(text)

      
def request_gpt(model=None, text="", temperature=0.5):

    check_and_create_path(model_path)
    check_and_create_path(openaiapi_path)
    

    with open(openaiapi_path, 'r') as f:
        openai.api_key = f.read().strip()

    
    with open(model_path, 'r') as f:
        model = f.read().strip()
    
    models = request_models()
    if model is None or model not in models:
        model = select_item_from_list(models)
        with open(model_path, 'w') as f:
            f.write(model)
           
    retrieve_response = openai.Model.retrieve(model)    
     
    n_tokens = num_tokens_from_string(text)
    tokens_limit = find_model_tokens_limit(model)
    
    if tokens_limit is None:
        tokens_limit = 4096#min
        
    if n_tokens > tokens_limit:
        text_chunks = split_text
        total_response = ""
        for chunk in text_chunks:
                completion = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": chunk}],
                temperature=temperature  # Here we set the temperature
                )
                total_response = total_response + completion["choices"][0]["message"]["content"]
        return total_response
               
    else:
        completion = openai.ChatCompletion.create(
         model=model,
         messages=[{"role": "user", "content": text}],
         temperature=temperature  # Here we set the temperature
         )
    
        return completion["choices"][0]["message"]["content"]

def request_models():
    
    check_and_create_path(openaiapi_path)
    
    with open(openaiapi_path, 'r') as f:
        openai.api_key = f.read().strip()# Define the headers for the request
        
    headers = {
        'Authorization': f'Bearer {openai.api_key}',
    }

    # Send a GET request to the OpenAI API
    response = requests.get('https://api.openai.com/v1/models', headers=headers)
    
    models = []
    check_response(response)
    
    for model_dict in response.json()['data']:
       
        models.append(model_dict['id'])
    
    return models
   
def check_response(response):
    response = str(response)
    if "200" not in response:
        raise Exception(response," Not valid request,see https://help.openai.com/en/collections/3808446-api-error-codes-explained")
    
     
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

def show_response_and_copy(root, response):
    # Create a top-level window
    top = tk.Toplevel(root)
    top.title("Response")

    # Add a Text widget to display the response
    text_widget = tk.Text(top, width=50, height=10)
    text_widget.insert(tk.END, response)
    text_widget.pack(padx=10, pady=10)

    # Add a button to copy the response
    copy_button = tk.Button(top, text="Copy", command=lambda: copy_to_clipboard(root, response))
    copy_button.pack(pady=10)
    
    
def check_and_create_path(path):
    if not os.path.exists(path):
        # create a root window
        root = tk.Tk()
        root.withdraw()  # hide the root window

        # ask the user if they want to create the path
        create_path = messagebox.askyesno(path+" does not exist", "Do you want to create the path?")
        if create_path:
            # get the text to write to the file
            text = simpledialog.askstring("Input", "What text do you want to write to the file?")
            
            # create the path and write the text to it
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(text)
        
        # destroy the root window
        root.destroy()
        
def request_gpt_prompt(user_input,temperature = 0.5):
    # Create the root window
    root = tk.Tk()
    root.withdraw()  # hide the root window

    
    print(user_input)
    if user_input:
        # Generate the response using GPT
        response = request_gpt(text=user_input, temperature=temperature)
        print(response)
        # Show the response in a custom window with a "Copy" button
        show_response_and_copy(root, response)

    # Run the tkinter event loop
    root.mainloop()
    root.destroy()
    
    #return response
    
def num_tokens_from_string(string: str, encoding_name=None:str) -> int:
    """Returns the number of tokens in a text string."""
    if encoding_name is None:
        encoding_name = "cl100k_base"
    
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def split_text(text,max_tokens):
    text_chunks = []
    n_chunks = math.ceil(max_tokens / num_tokens_from_string(text))
    return split_text_in_chunks(text,n_chunks)
    
def split_text_in_chunks(text, n_chunks):
    
    # Calculate the approximate chunk size
    chunk_size = len(text) // n_chunks

    chunks = []
    start_index = 0

    # Split the text into chunks
    for i in range(n_chunks - 1):
        end_index = start_index + chunk_size

        # Find the last dot within the chunk
        last_dot_index = text.rfind('.', start_index, end_index)
        if last_dot_index != -1:
            end_index = last_dot_index + 1

        # Add the chunk to the list
        chunks.append(text[start_index:end_index])

        # Move the start index to the next chunk
        start_index = end_index

    # Add the last chunk
    chunks.append(text[start_index:])

    return chunks   

if __name__ == "__main__":
    request_gpt(request_input())
