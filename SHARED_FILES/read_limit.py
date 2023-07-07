from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.common.by import By

import sys

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to the Python path
sys.path.insert(0, parent_dir)

# Specify the path to the model
base_path = os.getcwd()
model_path = os.path.join(base_path,"model.txt")

from SHARED_FILES.request_gpt import request_models

def find_model_tokens_limit(model=None):
    
    # Read the model
    if model is None:
        with open(model_path, 'r') as f:
            model = f.read().strip()

    # Determine the search name
    if "3.5" in model:
        search_name = "gpt-3-5"
    elif "4" in model:
        search_name = "gpt-4"
    else:
        return None
        
    # Formulate the URL
    url = "https://platform.openai.com/docs/models/" + search_name

    # Setup Chrome Service
    webdriver_service = Service(ChromeDriverManager().install())

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=webdriver_service)

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

                if model == row_elements[0].text and "token" in re.text:
                    max_tokens = int(re.text.split(" ")[0].replace(",",""))
                
    # Don't forget to close the driver
    driver.quit()

    print(max_tokens)

    return max_tokens
    
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
    for model in models:
    
    

        # Determine the search name
        #if "3.5" in model:
        #    search_name = "gpt-3-5"
        #elif "4" in model:
        #    search_name = "gpt-4"
        #else:
        #    models_limit[model]= min_tokens
        #    continue
        
        # Formulate the URL
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

                    if model == row_elements[0].text and "token" in re.text:
                        max_tokens = int(re.text.split(" ")[0].replace(",",""))
        
        if max_tokens is not None:
            models_limit[model]=max_tokens 
        else:
            models_limit[model]= min_tokens        
            
    #close the driver
    driver.quit()

    return models_list

print(find_models_tokens_limit())

