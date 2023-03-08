import openai
from os.path import exists, join
import os
import glob
import argparse

def get_transcript(recording_file_path : str) -> str:
    """
    Takes a complete path to a m4a voice memo and calls OpenAI Whisper API and returns transcript as string

    Parameter:
        recording_file_path (str): complete path to a m4a voice memo
    
    Returns:
        transcript (str): text transcript from Whisper
    """
    media_file = open(recording_file_path, 'rb')
    response = openai.Audio.transcribe(
        model='whisper-1',
        file=media_file,
        response_format='json',
        prompt="The is a transcript of an iPhone voice memo: "
    )
    return response

def save_text_file(output_path : str, content : str):
    """
    Writes content to a file at output path
    """
    with open(output_path, 'w') as f:
        f.write(content)

def get_m4a_files_in_dir(directory_path, max_mb = 25):
    """
    Yields all the m4a files in the directory that have a size at most max_mb
    """
    for file_path in glob.glob(os.path.join(directory_path, "*.m4a")):
        file_size = os.path.getsize(file_path) / (1024 * 1024) # convert bytes to MB
        if file_size <= max_mb:
            print(file_path)
            yield file_path

def transcribe_directory(directory_path, output_dir):
    """
    Transcribes each m4a file in directory path and saves a text file transcript with the same name in output_dir 
    """

    # Get paths for all m4a files in dir
    for _, file_path in enumerate(get_m4a_files_in_dir(directory_path)):
        # Get filename of m4a file without the .m4a ending
        file_basename = os.path.basename(file_path).split('.')[0]
        # Construct output path for m4a transcript
        output_txt_path = join(output_dir, file_basename + '.txt')
        # Already transcribed?
        if exists(output_txt_path):
            print(f'Transcript for {file_basename} already exists. Skipping.')
            continue
        # Compute size of m4a file in MB 
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        print(f'... {int(file_size)} MB')
        # Get transcript
        api_output = get_transcript(file_path)
        content = api_output['text']
        # Save the transcript
        save_text_file(output_txt_path, content)
        print(f'Saved transcript {file_basename}. Contents: {content}')

# Extra function that is not used which counts the total number of words transcribed
def count_words_in_directory(directory_path):
    total_word_count = 0
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r") as f:
                content = f.read()
                word_count = len(content.split())
                total_word_count += word_count
    return total_word_count

def main(input_dir, output_dir, api_key):
    print(f"Input directory: {input_dir}")
    assert exists(input_dir), "Input directory does not exist"
    print(f"Output directory: {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory '{output_dir}' created.")
    openai.api_key = api_key #'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'
    transcribe_directory(input_dir, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe iPhone voice memos with OpenAI Whisper API")
    parser.add_argument("-i", "--input_dir", help="Voice memos directory path")
    parser.add_argument("-o", "--output_dir", help="Output directory path with text transcripts")
    parser.add_argument("-api", "--openai_api_key", help="OpenAI API Key for Whisper API, find on platform.openai.com")
    args = parser.parse_args()
    main(args.input_dir, args.output_dir, args.openai_api_key)