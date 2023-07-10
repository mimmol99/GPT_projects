
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

def text_request(r_phrase = None,text=None,path_text=None,request_phrase=None):
    if text is None and (path_text is None or os.path.exists(path_text) is False):
        
        #while not path_text.endswith(".txt"):
        path_text = request_file_path("select txt")
       
    if text is None:
        with open(path_text, 'r') as file:
        # read the file content
            text = file.read()  
    #print("asking explanation")
    
    response = request_gpt(model=None,request_phrase = r_phrase,text=text)
    
    return response


if __name__ == "__main__":
    file_path = request_file_path()
    
    with open(file_path, 'r') as f:
    # read the file content
        text = f.read()
        
    
    response = text_request(r_phrase = "Genera delle domande a partire dal seguente testo: ",text = text)
    with open("./out.txt", 'w') as file:
    # read the file content
        file.write(response)
