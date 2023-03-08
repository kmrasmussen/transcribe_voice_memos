import openai
from os.path import exists, join
import os
import numpy as np
import glob
import pandas as pd
import hashlib
import argparse

def hash_string(input_string):
    """Return the SHA-256 hash of the input string"""
    encoded_string = input_string.encode('utf-8')
    hash_object = hashlib.sha256(encoded_string)
    return hash_object.hexdigest()

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   embd_list = openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
   return np.array(embd_list)
 
def read_text_files(directory_path):
    os.chdir(directory_path)
    for file_path in glob.glob("*.txt"):
        file_name2 = os.path.splitext(file_path)[0]
        with open(file_path, "r") as f:
            yield (file_name2, f.read())

def chunk_string(string, chunk_size, stride):
    offset = 0
    while offset < len(string):
        yield (offset, string[offset:offset+chunk_size])
        offset += stride

def embed_transcripts(transcripts_dir, output_json, chunk_size, stride) -> pd.DataFrame:
    if exists(output_json):
        print(f'{output_json} already exists, will add unembdded transcripts to file')
        df = pd.read_json(output_json)
        print(f'Number of embeddings already: {len(df)}')
    else:
        df = None
    chunk_dicts = []
    for _, (file_path, content) in enumerate(read_text_files(transcripts_dir)):
        if content == '':
            content = 'empty string'
        print(file_path, content)
        transcript_hash = hash_string(content)
        print('chunks:')
        for offset, chunk_content in chunk_string(content, chunk_size, stride):
            print(offset, chunk_content)
            transcript_chunk_hash = hash_string(chunk_content)
            if df is not None and any(df['chunk_hash'] == transcript_chunk_hash):
                break
            chunk_embedding = get_embedding(chunk_content)
            chunk_dict = {
                'voice_memo_name': file_path,
                'transcript_hash': transcript_hash,
                'offset': offset,
                'chunk_hash': transcript_chunk_hash,
                'chunk_content': chunk_content,
                'chunk_embedding': chunk_embedding
            }
            chunk_dicts.append(chunk_dict)
    df_new = pd.DataFrame(chunk_dicts)
    print(f'Number of new embeddings: {len(df_new)}')
    if df is not None:
        return pd.concat([df, df_new], ignore_index='index')
    else:
        return df_new

def main(input_dir, output_file, api_key, chunk_size, stride):
    work_dir = os.getcwd()
    print(f"Input directory: {input_dir}")
    assert exists(input_dir), "Input directory does not exist"
    openai.api_key = api_key 
    df_embeddings = embed_transcripts(input_dir, output_file, chunk_size, stride)
    os.chdir(work_dir)
    print(f'Saving embeddings to {output_file}', os.getcwd())
    df_embeddings.to_json(output_file)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Transcribe iPhone voice memos with OpenAI Whisper API")
    parser.add_argument("-i", "--input_dir", help="Transcripts directory path")
    parser.add_argument("-o", "--output_file", help="Output JSON file to save dataframe")
    parser.add_argument("-api", "--openai_api_key", help="OpenAI API Key for Whisper API, find on platform.openai.com")
    parser.add_argument("-chunk", "--chunk_size", type=int, default=1500, help="Chunk size when dividing transcript up into chunks and embedding separately")
    parser.add_argument("-stride", "--stride_length", type=int, default=500, help="Stride when dividing transcripts up into chunks")
    args = parser.parse_args()
    main(args.input_dir, args.output_file, args.openai_api_key, args.chunk_size, args.stride_length)