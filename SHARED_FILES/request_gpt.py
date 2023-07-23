import re
import time
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
import PyPDF2
from docx import Document
from tqdm import tqdm
from pptx import Presentation
nltk.download('punkt')

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to the Python path
sys.path.insert(0, parent_dir)


from SHARED_FILES.directory_request import request_string,request_file_paths

class GPTRequester:
    

    def __init__(self) -> None:
        
        self.base_path = os.getcwd()
        self.model_path = os.path.join(self.base_path,"model.txt")
        self.openaiapi_path = os.path.join(self.base_path,"openaiapi.txt")
        self.check_and_create_path(self.model_path)
        self.check_and_create_path(self.openaiapi_path)
        self.file_extensions_available = [".txt",".doc",".docx",".pdf",".pptx"]

        with open(self.openaiapi_path, 'r') as f:
            openai.api_key = f.read().strip()
    
        with open(self.model_path, 'r') as f:
            self.model = f.read().strip()

        self.models_limit_path = os.path.join(self.base_path,"models_limit.json")

        if not os.path.exists(self.models_limit_path):
            self.find_models_tokens_limit()

        
    def request_gpt(self,model=None, request_phrase = "",text="", temperature=0.5):
        min_tokens = 2048
        

        
        models = self.request_models()
    
        if model is None or model not in models:
            model = self.select_item_from_list(models)
            with open(self.model_path, 'w') as f:
                f.write(model)
            
        models_limit = {}
        
        if os.path.exists(self.models_limit_path):
            with open(self.models_limit_path, 'r') as json_file:
                models_limit = json.load(json_file)
                
            if len(models)!=len(models_limit.keys()):
                models_limit = self.find_models_tokens_limit()
        else:
            models_limit = self.find_models_tokens_limit()
        
  
        openai.Model.retrieve(model)   

        n_tokens = self.num_tokens_from_string(text) * 2 #to leave response space  
        tokens_limit = models_limit[model] //  2
        
        if n_tokens > tokens_limit:
            text_chunks = self.split_text(text,tokens_limit)
            total_response = ""
            for chunk in text_chunks:
                    try:
                        completion = openai.ChatCompletion.create(
                        model=model,
                        messages=[{"role": "user", "content":request_phrase+ chunk}],
                        temperature=temperature  # Here we set the temperature
                        )
                        total_response = total_response + completion["choices"][0]["message"]["content"]
                        openai.Model.retrieve(model)
                    except ServiceUnavailableError:
                        time.sleep(10)
                        total_response = total_response + self.request_gpt(model=model, request_phrase = request_phrase,text=chunk, temperature=0.5)
                    
            return total_response
                
        else:
            try:
                completion = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content":request_phrase+text}],
                temperature=temperature  # Here we set the temperature
                )
                response = completion["choices"][0]["message"]["content"]
                openai.Model.retrieve(model)
            except ServiceUnavailableError:
                time.sleep(10)
                response = self.request_gpt(model=model, request_phrase = request_phrase,text=text, temperature=0.5)

            return response

    def request_gpt_translation(self,model="text-davinci-003",text="", temperature=0.5):
        min_tokens = 2048
        
        
        models = self.request_models()
    
        if model is None or model not in models:
            model = self.select_item_from_list(models)
            with open(self.model_path, 'w') as f:
                f.write(model)
            
        models_limit = {}
        
        if os.path.exists(self.models_limit_path):
            with open(self.models_limit_path, 'r') as json_file:
                models_limit = json.load(json_file)
                
            if len(models)!=len(models_limit.keys()):
                models_limit = self.find_models_tokens_limit()
        else:
            models_limit = self.find_models_tokens_limit()
        
        
        retrieve_response = openai.Model.retrieve(model)        
        n_tokens = self.num_tokens_from_string(text) * 2 #to leave response space  
        tokens_limit = models_limit[model]
        
        if n_tokens > tokens_limit:
            text_chunks = self.split_text(text,tokens_limit)
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
        
    def select_item_from_list(self,item_list):
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
        
        
    def check_and_create_path(self,path):
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
            
        
    def num_tokens_from_string(self,string, encoding_name=None):
        """Returns the number of tokens in a text string."""
        if encoding_name is None:
            encoding_name = "cl100k_base"
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def split_text(self,text, max_tokens):
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
  

    def find_model_tokens_limit(self,model=None):
        
        # Read the model
        if model is None:
            with open(self.model_path, 'r') as f:
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

        
    def find_models_tokens_limit(self):
        
        models = self.request_models()
        
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
        
        with open(self.models_limit_path, 'w') as json_file:
            json.dump(models_limit, json_file)

        return models_limit
    

    def file_to_text(self,file_path):
        _, file_extension = os.path.splitext(file_path)

        text = ""

        if file_extension in self.file_extensions_available:
            if file_extension == ".pdf":
                text = self.pdf_to_text(file_path)
            elif file_extension in [".doc", ".docx"]:
                text = self.docx_to_text(file_path)
            elif file_extension == ".txt":
                text = self.txt_to_text(file_path)
            elif file_extension == ".pptx":
                text = self.pptx_to_text(file_path)
        else:
            print(f"File type {file_extension} is not supported. Supported: {self.file_extensions_available}")
            return None

        return text

    def txt_to_text(self,path):
        with open(path, 'r') as file:
            return file.read()

    def pdf_to_text(self,file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            text = ''
            
            for page in reader.pages:
                text += page.extract_text()
            
        return text

    def docx_to_text(self,path):
        doc = Document(path)
        fullText = []
        for paragraph in doc.paragraphs:
            fullText.append(paragraph.text)
        return '\n'.join(fullText)

    def pptx_to_text(self,path):
        pres = Presentation(path)
        text = ''
        for slide in pres.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text
        return text
    

    def request_all_files(self,model=None,request_phrase="",document_name="output"):

        files = request_file_paths("select files")
        document = Document()
        requester = GPTRequester()
        pbar = tqdm(files, desc="Processing files")

        for f_path in pbar:
            base_name = os.path.basename(f_path).split(".")[0]
            pbar.set_description(f"Processing {base_name}")
            text = self.file_to_text(f_path)
            if text is None:continue
            response = requester.request_gpt(model = None,request_phrase=request_phrase,text=text)
            document.add_heading(document_name, level=1)
            document.add_paragraph(response)

        document.save(document_name+".docx")
    
    
    
if __name__ == "__main__":
    #print(request_gpt_translation(model="ada",text="As of March 1, 2023, data sent to the OpenAI API will not be used to train or improve OpenAI models (unless you explitly opt in). One advantage to opting in is that the models may get better at your use case over time."))
    requester = GPTRequester()
    requester.request_all_files(request_phrase=request_string("Insert gpt prompt"),document_name=request_string("insert document name"))