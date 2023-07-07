
import sys
import os
# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to the Python path
sys.path.insert(0, parent_dir)

from SHARED_FILES.request_input import request_input
from SHARED_FILES.directory_request import request_file_path,request_folder_path
from SHARED_FILES.divide_text_into_chunks import divide_text_into_chunks
from SHARED_FILES.request_gpt import request_gpt

def text_explanation(text=None,path_text=None,request_phrase=None):
    if text is None and (path_text is None or os.path.exists(path_text) is False):
        
        #while not path_text.endswith(".txt"):
        path_text = request_file_path("select txt")
       
    if text is None:
        with open(path_text, 'r') as file:
        # read the file content
            text = file.read()  
    #print("asking explanation")
    if not request_phrase:
        request_phrase = "Spiega il seguente testo come se fosse un riassunto da far leggere ad uno studente: "
    response = request_gpt(model=None,text=request_phrase+text)
    
    return response


if __name__ == "__main__":
    text = text_explanation()
    with open("./out.txt", 'w') as file:
    # read the file content
        file.write(text)
