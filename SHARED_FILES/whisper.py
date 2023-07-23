import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import openai
from divide_audio import divide_audio
from request_gpt import request_gpt
from docx import Document
from docx.shared import Inches
from SHARED_FILES.graphic_request import request_file_path,request_file_paths
from tkinter import Tk,simpledialog,filedialog



def clean_text(text):
	pass

def transcript_audio(audio_path):
    audio_file= open(audio_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text = transcript["text"]
    return text
    
def write_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)

        
def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path,'r') as f:
            file_text = f.read().strip()
            f.close()
        return file_text
    else:
        print("File path not exists")
        return None
    
def merge_audio_files(audio_paths):
    format_audio = os.path.basename(audio_paths[0]).split(".")[1]
    combined_audio = AudioSegment.from_file(audio_paths[0], format=format_audio)
        
    for audio in audio_paths[1:]:
        format_audio = os.path.basename(audio).split(".")[1]
        combined_audio+=AudioSegment.from_file(audio, format=format_audio)
            
    combined_audio.export("./combined_audio."+str(format_audio),format=format_audio)
    audio_path = "./combined_audio."+str(format_audio)
    return audio_path

def ask_save_folder(title):
    root = Tk()
    root.withdraw()
    save_path = filedialog.askdirectory(title=title)
    return save_path


if __name__ == "__main__":
    api_key_file_path = "./api_key.txt"
    title_window_ask_audio_files = "select audio file(s)"
    
    root = Tk()
    root.withdraw()
    
    if not os.path.exists(api_key_file_path):
        #open a window to insert the api key
        api_key = simpledialog.askstring(title = "insert API ChatGPT",prompt="key",parent=root)
        write_file(api_key_file_path, api_key)
    else:
        api_key = read_file(api_key_file_path)
        
    #open a window to select the audio file
    openai.api_key = api_key#"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"
    
    #open a window to select the audio file
    audio_paths = request_file_paths(title=title_window_ask_audio_files)
    
    if len(audio_paths)>1:
        audio_path = merge_audio_files(audio_paths)
    else:
        audio_path = audio_paths[0]
            
    
    #find audio name and type
    audio_folder_path = ask_save_folder(title = "Choose where to save transcription and summarization")#os.path.split(audio_path)[0]
    print(audio_folder_path)
    name_audio = os.path.basename(audio_path).split(".")[0]
    type_audio = os.path.basename(audio_path).split(".")[1]
    
    #create a folder to save the chunks
    chunks_path = os.path.join(os.path.split(audio_path)[0],"chunks_"+str(name_audio))
    
    #create a path for the transcription and summarization docx
    transcription_path = os.path.join(audio_folder_path,name_audio+"_transcription.docx")
    after_chatgpt_path = os.path.join(audio_folder_path,name_audio+"_after_gpt.docx")
    
    #what ask to chat gpt
    chatgpt_request = "Riscrivi e dividi in sezioni questo testo: "
    
    #divide audio file in chunks due to max size per audio of whisper model
    divide_audio(audio_path)
    

    if not os.path.exists(transcription_path):
        print("Transcripting chunks..")
        text = ""
        for i,chunk in enumerate(os.listdir(chunks_path)):
            print("transcripting chunk ",i+1," on ",len(os.listdir(chunks_path)))
            chunk_path = os.path.join(chunks_path,name_audio+"_chunk"+str(i)+"."+str(type_audio))
            text = text + transcript_audio(chunk_path)
        document = Document()
        document.add_heading('Transcription '+str(name_audio), level=0)
        document.add_paragraph(text)
        document.save(transcription_path)
    else:
        document = Document(transcription_path)
        text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
        print("transcription file already exists")


    
    if not os.path.exists(after_chatgpt_path):
        print("requesting chatGPT..")
        max_tokens = 4096
        num_requests = len(text) // max_tokens + 1
        text_gpt  = ""
        for i in range(num_requests):
            text_gpt = text_gpt + request_gpt(chatgpt_request+text[i*max_tokens:(i+1)*max_tokens] )
        document = Document()
        document.add_heading('After chatGPT '+str(name_audio), level=0)
        document.add_paragraph(text_gpt)
        document.save(after_chatgpt_path)
    else:
        print("chatGPT text file alredy exists") 
        
    #remove the combined
    if len(audio_paths)>1:
        os.remove(audio_path)
    
    #remove the chunks folder
    os.remove(chunks_path)
    
        
    
    
    

    
