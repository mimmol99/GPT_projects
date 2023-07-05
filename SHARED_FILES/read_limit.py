from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.common.by import By

# Specify the path to the model
base_path = os.getcwd()
model_path = os.path.join(base_path,"model.txt")


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

find_model_tokens_limit(model=None)