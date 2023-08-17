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


def transcript_audio(audio_path):
    audio_file= open(audio_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text = transcript["text"]
    return text
    
    
def merge_audio_files(audio_paths):
    format_audio = os.path.basename(audio_paths[0]).split(".")[1]
    combined_audio = AudioSegment.from_file(audio_paths[0], format=format_audio)
        
    for audio in audio_paths[1:]:
        format_audio = os.path.basename(audio).split(".")[1]
        combined_audio+=AudioSegment.from_file(audio, format=format_audio)
            
    combined_audio.export("./combined_audio."+str(format_audio),format=format_audio)
    audio_path = "./combined_audio."+str(format_audio)
    return audio_path


    
        
    
    
    

    
