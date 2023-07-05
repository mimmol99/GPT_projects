from selenium import webdriver
import os

# Specify the path to the webdriver
webdriver_path = '/home/domenico/Desktop/PERSONAL/Projects/Chromedriverselenium'  

# Specify the path to the model
base_path = os.getcwd()
model_path = os.path.join(base_path,"model.txt")

# Read the model
with open(model_path, 'r') as f:
    model = f.read().strip()

# Determine the search name
if "3.5" in model:
    search_name = "gpt-3-5"
elif "4" in model:
    search_name = "gpt-4"

# Formulate the URL
url = "https://platform.openai.com/docs/models/" + search_name

# Create a new instance of the Firefox driver
driver = webdriver.Chrome(executable_path=webdriver_path)

# Go to the OpenAI documentation page
driver.get(url)

# Get all tables with the class 'models-table'
models_tables = driver.find_elements_by_xpath('//table[@class="models-table"]')

# Process the models-table objects
for table in models_tables:
    # Find all rows in the table, skipping the first one (header)
    rows = table.find_elements_by_tag_name('tr')[1:]

    for row in rows:
        # Get all columns
        columns = row.find_elements_by_tag_name('td')

        # Extract model name and description from the columns
        model_name = columns[0].text
        model_description = columns[1].text

        # Print the extracted information
        print(f"Model: {model_name}")
        print(f"Description: {model_description}")
        print("-" * 50)

# Don't forget to close the driver
driver.quit()


