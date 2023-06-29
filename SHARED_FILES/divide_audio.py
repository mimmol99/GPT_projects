from pydub import AudioSegment
import os

#divide a file in chunks of max 24 mb

def divide_audio(audio_path):
	
    type_audio = os.path.basename(audio_path).split(".")[1]
    name_audio = os.path.basename(audio_path).split(".")[0]
    acceptable_formats = ["mp3","mp4","mpeg", "mpga", "wav", "webm"]
    if type_audio not in acceptable_formats:
	    raise ValueError(type_audio, " not an acceptable format: ",acceptable_formats)
	
    audio = AudioSegment.from_file(audio_path, format=type_audio)
    size = os.path.getsize(audio_path)
    max_len = 24000000
    chunks = round(size/max_len)
    per_chunk = len(audio)/chunks
    print("Splitting audio..")
    chunk_list = []
    path_to_save = os.path.join(os.path.split(audio_path)[0],"chunks_"+str(name_audio))
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    else:
        if len(os.listdir(path_to_save))==chunks:
            print("chunks already found")
            return
            
    for i in range(chunks):
        print("splitting:" ,i ," on ",chunks)
        chunk_audio = audio[i*per_chunk:(i+1)*per_chunk]
        chunk_audio.export(os.path.join(path_to_save,name_audio+"_chunk"+str(i)+"."+str(type_audio)), format=type_audio)
	    
    
		
#if __name__ == "__main__":
#    divide_audio("./AUDIO/AUTONOMOUS/3_8/")

