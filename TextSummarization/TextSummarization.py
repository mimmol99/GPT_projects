from request_input import request_input
from directory_request import request_file_path,request_folder_path
from divide_text_into_chunks import divide_text_into_chunks

from summarize_directory import summarize_directory

def main():
    path_txt = request_folder_path(title="select the folder with chunks to summarize")
    #with open(path_txt, 'r') as file:
    #    content = file.read()
    #
    #divide_text_into_chunks(content,file_name='document_to_be_summarized',chunk_size=1500)
    summarize_directory(path_txt)
    
if __name__ == "__main__":
	
    main()
