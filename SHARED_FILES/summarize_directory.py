import os
import openai
from request_gpt import request_gpt
from tqdm import tqdm

def summarize_directory(directory_path, summarized_directory_path=None):
    summarized_text = ""
    
    filenames = [f for f in os.listdir(directory_path) if f.endswith('.txt') and "chunk" in f]
    
    # Sort filenames based on the number before '.txt'
    filenames = sorted(filenames, key=lambda f: int(f.rsplit('_', 1)[1].split('.')[0]))
    
    # If no summarized directory path is provided, use the current directory
    if summarized_directory_path is None:
        summarized_directory_path = os.path.join(os.getcwd(), "summarized_folder")
    
    # Create the summarized directory if it doesn't exist
    os.makedirs(summarized_directory_path, exist_ok=True)
    
    for filename in tqdm(filenames, desc="Summarizing files"):
        new_filename = f"summarized_{filename}"
        new_file_path = os.path.join(summarized_directory_path, new_filename)

        # Check if the summarized file already exists
        if os.path.exists(new_file_path):
            # If it does, read it and add it to the summarized text
            with open(new_file_path, 'r') as file:
                summarized_text = file.read()
            print(f"Summarized file {new_filename} already exists, reading it.")
        else:
            # If it doesn't, read the original text and request the translation
            with open(os.path.join(directory_path, filename), 'r') as file:
                original_text = file.read()

            string_request = "Riassumi in italiano il seguente testo:"+original_text
            summarized_text += request_gpt(string_request)

            # Save the translated text
            with open(new_file_path, 'w') as file:
                file.write(summarized_text)
            print(f"Summarized file {new_filename} created.")
