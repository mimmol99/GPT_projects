from request_input import request_input
from directory_request import request_file_path
from divide_text_into_chunks import divide_text_into_chunks
from request_gpt import request
from translate_directory import translate_directory

def main():
    path_txt = request_file_path(title="select the txt to translate")
    with open(path_txt, 'r') as file:
        content = file.read()
    #original_language = request_input(title="Translate",prompt="insert original text language",default_value="english")
    #translated_language = request_input(title="Translate",prompt="insert language to be translated",default_value="italian")
    divide_text_into_chunks(content,file_name='document_to_be_translated',chunk_size=1500)
    #translate_directory('chunks_'+'document_to_be_translated')#,original_language,translated_language)
    
if __name__ == "__main__":
	
    main()
