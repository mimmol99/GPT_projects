
import sys

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to the Python path
sys.path.insert(0, parent_dir)

from SHARED_FILES.directory_request import request_file_path
from SHARED_FILES.divide_text_into_chunks import divide_text_into_chunks
import os

import PyPDF2

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ''
        
        for page in reader.pages:
            text += page.extract_text()
        
    return text
    
def main():
    path_pdf = request_file_path(title="select the PDF from to extract text")
    pdf_name = os.path.basename(path_pdf)
    text_pdf = extract_text_from_pdf(file_path=path_pdf)

    # Write text_pdf to a text file
    output_file_path = os.path.splitext(pdf_name)[0] + ".txt"
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(text_pdf)
        
if __name__ == "__main__":
	
    main()
