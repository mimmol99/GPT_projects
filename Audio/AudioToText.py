import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import openai

import sys

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to the Python path
sys.path.insert(0, parent_dir)

from SHARED_FILES.divide_audio import divide_audio
from SHARED_FILES.request_gpt import request_gpt,transcript_audio
from SHARED_FILES.directory_request import request_file_paths
from SHARED_FILES.recognize_speech import audio_text

from tqdm import tqdm



if __name__ == "__main__":
    audio_paths = request_file_paths(title="select one (or more) audio")
    
    total_text = ""
    
    # Create a progress bar
    progress_bar = tqdm(audio_paths, desc="Transcribing Audio", unit="audio")

    for audio_path in progress_bar:
        name_audio = os.path.basename(audio_path).split(".")[0]
        type_audio = os.path.basename(audio_path).split(".")[1]
    
        text = transcript_audio(audio_path)
        total_text += text

    with open(name_audio + "_transcription.txt", 'w') as file:
        file.write(text)
    
    if len(audio_paths) > 1:
        with open(name_audio + "_merged.txt", 'w') as file:
            file.write(total_text)
    
    # Uncomment the following code if you want to include the GPT request progress bar
    '''
    max_tokens = 4096
    num_requests = len(text) // max_tokens + 1
    text_gpt = ""
    print("Requesting CHATgpt...")
    
    # Create a progress bar for GPT requests
    progress_bar = tqdm(range(num_requests), desc="GPT Requests", unit="request")
    
    for i in progress_bar:
        text_gpt = text_gpt + request_gpt("Riscrivi questo testo in appunti universitari: " + text[i * max_tokens:(i + 1) * max_tokens])
    
    with open(name_audio + "_after_gpt.txt", 'a') as file:
        file.write(text_gpt)
    '''


