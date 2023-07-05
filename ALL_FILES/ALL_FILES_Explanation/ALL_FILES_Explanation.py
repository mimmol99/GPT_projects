
import sys
import os
import PyPDF2

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to the Python path
sys.path.insert(0, parent_dir)

from SHARED_FILES.directory_request import request_file_path,request_file_paths
from SHARED_FILES.divide_text_into_chunks import divide_text_into_chunks
from PDF.PDFtoText import pdf_to_text
from PPT.PPT_explanation.PPT_explanation import explain_pptx
from TXT.TextExplanation.TextExplanation import text_explanation 

def main():
    files = request_file_paths("select files")
    total_text = ""
    for f_path in files:
        if f_path.endswith(".txt"):
            total_text += text_explanation(path_text=f_path)
        elif f_path.endswith(".pptx"):
            text = explain_pptx(f_path)
            total_text += text_explanation(text=text)
        elif f_path.endswith(".pdf"):
            text = pdf_to_text(f_path)
            total_text += text_explanation(text=text)
    
    with open("./out.txt", 'w') as file:
    # read the file content
        file.write(total_text)         
            
            
            
        
    
    
        
if __name__ == "__main__":
    main()
