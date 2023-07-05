
import sys
import os
import PyPDF2

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to the Python path
sys.path.insert(0, parent_dir)

from SHARED_FILES.directory_request import request_file_path
from SHARED_FILES.divide_text_into_chunks import divide_text_into_chunks


def pdf_to_text(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ''
        
        for page in reader.pages:
            text += page.extract_text()
        
    return text
    
def main():
    paths_pdf = request_file_paths(title="select the PDF from to extract text")
    text_pdf = ""
    for path_pdf in paths_pdf:
        
        text_pdf += pdf_to_text(file_path=path_pdf)

    # Write text_pdf to a text file
    
    with open("./pdf_output.txt", "w", encoding="utf-8") as output_file:
        output_file.write(text_pdf)
        
if __name__ == "__main__":
	
    main()
