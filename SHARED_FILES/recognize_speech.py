import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

def audio_text(file_path):
    r = sr.Recognizer()
    chunks = []
    sound = AudioSegment.from_wav(file_path)
    chunk_duration_ms = 10000
    chunks = []
    for i in range(0, len(sound), chunk_duration_ms):
        chunk = sound[i:i+chunk_duration_ms]
        chunks.extend(split_on_silence(chunk, min_silence_len=1000, silence_thresh=-40, keep_silence=1000))
    text = ""
    chunks_count = 0
    for i, chunk in enumerate(chunks):
        chunk_audio = sr.AudioData(chunk._data, sound.frame_rate, sound.sample_width)
        try:
            text += r.recognize_google(chunk_audio,language = 'it-IT')
            chunks_count += 1
            print(f"Number of chunks processed: {chunks_count}")
            print("Text: ", text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return text

def main():
    file_path = '/home/domenico/Downloads/WhatsApp.wav'
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        return
    text = audio_text(file_path)
    print("Transcription: " + text)

if __name__ == "__main__":
    main()
    

    
