import openai
import tkinter as tk
from tkinter import  simpledialog,messagebox
import requests
import os
import tiktoken
import math
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import sys
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

def split_text(text, max_tokens):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = ''

    for sentence in sentences:
        # If adding the next sentence doesn't exceed the maximum token limit
        if len(current_chunk) + len(sentence) <= max_tokens:
            current_chunk += ' ' + sentence
        else:
            # Add the current chunk to the list
            chunks.append(current_chunk.strip())
            # Start a new chunk with the current sentence
            current_chunk = sentence
            
    # Don't forget to add the last chunk
    chunks.append(current_chunk.strip())

    return chunks


# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to the Python path
sys.path.insert(0, parent_dir)

base_path = os.getcwd()
model_path = os.path.join(base_path,"model.txt")
openaiapi_path = os.path.join(base_path,"openaiapi.txt")
models_limit_path = os.path.join(base_path,"models_limit.json")

from SHARED_FILES.request_input import request_input
#from SHARED_FILES.read_limit import find_model_tokens_limit

def copy_to_clipboard(root, text):
    # Clear the clipboard
    root.clipboard_clear()
    # Copy the text to the clipboard
    root.clipboard_append(text)

      
def request_gpt(model=None, request_phrase = "",text="", temperature=0.5):
    min_tokens = 2048
    
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
           
    models_limit = {}
    
    if os.path.exists(models_limit_path):
        with open(models_limit_path, 'r') as json_file:
            models_limit = json.load(json_file)
            
        if len(models)!=len(models_limit.keys()):
            models_limit = find_models_tokens_limit()
    else:
        models_limit = find_models_tokens_limit()
     
    
    retrieve_response = openai.Model.retrieve(model)        
    n_tokens = num_tokens_from_string(text) * 2 #to leave response space  
    tokens_limit = models_limit[model] //  2
    
    if n_tokens > tokens_limit:
        text_chunks = split_text(text,tokens_limit)
        total_response = ""
        for chunk in text_chunks:
                completion = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content":request_phrase+ chunk}],
                temperature=temperature  # Here we set the temperature
                )
                total_response = total_response + completion["choices"][0]["message"]["content"]
                openai.Model.retrieve(model)
                
        return total_response
               
    else:
        completion = openai.ChatCompletion.create(
         model=model,
         messages=[{"role": "user", "content":request_phrase+ text}],
         temperature=temperature  # Here we set the temperature
         )
    
        return completion["choices"][0]["message"]["content"]

def request_gpt_translation(model="text-davinci-003",text="", temperature=0.5):
    min_tokens = 2048
    
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
           
    models_limit = {}
    
    if os.path.exists(models_limit_path):
        with open(models_limit_path, 'r') as json_file:
            models_limit = json.load(json_file)
            
        if len(models)!=len(models_limit.keys()):
            models_limit = find_models_tokens_limit()
    else:
        models_limit = find_models_tokens_limit()
     
    
    retrieve_response = openai.Model.retrieve(model)        
    n_tokens = num_tokens_from_string(text) * 2 #to leave response space  
    tokens_limit = models_limit[model]
    
    if n_tokens > tokens_limit:
        text_chunks = split_text(text,tokens_limit)
        total_response = ""
        for chunk in text_chunks:
                completion =  openai.Completion.create(
  model="text-davinci-003",
  prompt="Translate this into Italian:\n\n "+text+" \n\n.",
  temperature=temperature,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0)
                total_response = total_response + completion["choices"][0]["text"]
                
        return total_response
               
    else:
        completion = openai.Completion.create(
  model="text-davinci-003",
  prompt="Translate this into Italian:\n "+text+".",
  temperature=temperature,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0)
        
        return completion["choices"][0]["text"]
def request_models_old():
    
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
    
def request_models():
    
    check_and_create_path(openaiapi_path)
    
    with open(openaiapi_path, 'r') as f:
        openai.api_key = f.read().strip()# Define the headers for the request
        
    models = [model_dict["id"] for model_dict in openai.Model.list()["data"]]
    
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
    
def num_tokens_from_string(string, encoding_name=None):
    """Returns the number of tokens in a text string."""
    if encoding_name is None:
        encoding_name = "cl100k_base"
    
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def split_text(text, max_tokens):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = ''

    for sentence in sentences:
        # If adding the next sentence doesn't exceed the maximum token limit
        if len(current_chunk) + len(sentence) <= max_tokens:
            current_chunk += ' ' + sentence
        else:
            # Add the current chunk to the list
            chunks.append(current_chunk.strip())
            # Start a new chunk with the current sentence
            current_chunk = sentence
            
    # Don't forget to add the last chunk
    chunks.append(current_chunk.strip())

    return chunks
"""
def split_text(text,max_tokens):
    text_chunks = []
    n_chunks = math.ceil(max_tokens / num_tokens_from_string(text))
    return split_text_in_chunks(text,n_chunks)
""" 
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

def find_model_tokens_limit(model=None):
    
    # Read the model
    if model is None:
        with open(model_path, 'r') as f:
            model = f.read().strip()
            
    min_tokens = 2048
    
    
    # Setup Chrome Service
    webdriver_service = Service(ChromeDriverManager().install())
    
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=webdriver_service)
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=webdriver_service)
    
    url = "https://platform.openai.com/docs/models/" 

    # Go to the OpenAI documentation page
    driver.get(url)

    # Get all tables with the class 'models-table'
    models_tables = driver.find_elements(By.CLASS_NAME,"models-table")

    max_tokens = None
    
    # Process the models-table objects
    for table in models_tables:
        # Find all rows in the table, skipping the first one (header)

        rows = table.find_elements(By.CSS_SELECTOR,'tr')

        for row in rows:

            row_elements = row.find_elements(By.CSS_SELECTOR,"td")
            for re in row_elements:
                current_model = row_elements[0].text
                if current_model == model and "token" in re.text:
                    max_tokens = int(re.text.split(" ")[0].replace(",",""))
                    return max_tokens
                    
                    
    #close the driver
    driver.quit()
    
    return min_tokens

    
def find_models_tokens_limit():
    
    models = request_models()
    
    min_tokens = 2048
    
    models_limit = {}
    
    # Setup Chrome Service
    webdriver_service = Service(ChromeDriverManager().install())
    
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=webdriver_service)
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=webdriver_service)
    
    url = "https://platform.openai.com/docs/models/" 

    # Go to the OpenAI documentation page
    driver.get(url)

    # Get all tables with the class 'models-table'
    models_tables = driver.find_elements(By.CLASS_NAME,"models-table")

    max_tokens = None
    
    # Process the models-table objects
    for table in models_tables:
        # Find all rows in the table, skipping the first one (header)

        rows = table.find_elements(By.CSS_SELECTOR,'tr')

        for row in rows:

            row_elements = row.find_elements(By.CSS_SELECTOR,"td")
            for re in row_elements:
                current_model = row_elements[0].text
                if current_model in models and "token" in re.text:
                    max_tokens = int(re.text.split(" ")[0].replace(",",""))
                    models_limit[current_model]= max_tokens 
                    #print(models_limit)
                    
    #close the driver
    driver.quit()
    
    for model in models:
        if model not in models_limit.keys():
            models_limit[model]= min_tokens  
       
            
    
    #print(models_limit)
    
    with open(models_limit_path, 'w') as json_file:
        json.dump(models_limit, json_file)

    return models_limit
    
    
    
if __name__ == "__main__":
    print(request_gpt_translation(model="ada",text="As of March 1, 2023, data sent to the OpenAI API will not be used to train or improve OpenAI models (unless you explitly opt in). One advantage to opting in is that the models may get better at your use case over time."))
