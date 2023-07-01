import os
import openai
from request_gpt import request
#from googletrans import Translator
from translate import Translator


def translate_files_in_directory(directory_path,file_types = ((".txt")), original_language='english', translated_language='italian'):
    translator = Translator(from_lang="english", to_lang="italian")
    # Iterate over all .txt files in the specified directory
    translated_text = ""
    for filename in os.listdir(directory_path):
        if filename.endswith(file_types):
            # Read the original text
            with open(os.path.join(directory_path, filename), 'r') as file:
                original_text = file.read()

            # Request the translation
            #prompt = "Translate the following text from "+original_language+" to "+translated_language+": "+original_text
            #print(prompt)
            translated_text = translated_text +  translator.translate(original_text)

            # Save the translated text
    new_filename = f"translated_{filename}"
    with open(os.path.join(directory_path, new_filename), 'w') as file:
        file.write(translated_text)
        
def translate_text(text, original_language='english', translated_language='italian'):
    translator = Translator(from_lang="english", to_lang="italian")
    # Iterate over all .txt files in the specified directory
    return translator.translate(original_text)
    


