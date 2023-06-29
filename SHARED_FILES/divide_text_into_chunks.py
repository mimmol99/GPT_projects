import os
import nltk

def divide_text_into_chunks(text, file_name,chunk_size=2000):
    nltk.download('punkt')  # Download the Punkt tokenizer, if not already downloaded.
    tokens = nltk.word_tokenize(text)  # Tokenize the input text
    
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]  # Break the tokens into chunks
	
	    
    # Create the output directory if it doesn't exist
    output_dir = 'chunks_' + file_name
    os.makedirs(output_dir, exist_ok=True)

    # Save the entire text first
    with open(os.path.join(output_dir, f'{file_name}_entire_text.txt'), 'w') as entire_text_file:
        entire_text_file.write(text)
    # Write each chunk to a new file
    for i, chunk in enumerate(chunks):
        with open(os.path.join(output_dir, f'{file_name}_chunk_{i}.txt'), 'w') as chunk_file:
            chunk_file.write(' '.join(chunk))
