# transcribe voice memos
This Python script takes 3 inputs
* Input directory containing your voice memos. Find this directory by going to iTunes, sync with your iPhone, go to Voice memos, right click on a voice memo and click show in Finder.
* Output directory: If it does not exist it will be created for you. It will contain .txt files with the same names as the voice memo .m4a audio recording
* OpenAI api key: The voice memos are trancribed using OpenAI Whisper speech to text API. Go to platform. Sign up and get an API key at [openai.com](https://platform.openai.com/account/api-keys)

# Usage
```
python3 transcribe_memos.py -i /Users/kasperrasmussen/Music/iTunes/iTunes\ Media/Voice\ Memos -o ./transcripts/ -api <open_ai_api_key>
```

# Embeddings
*embed_transcripts.py* allows for using OpenAI Embeddings API to create vector embeddings for the transcripts. Each transcript is divided into smaller chunks, one embedding vector per chunk of a transcript.

The result will be a Pandas dataframe that is stored as JSON with one row per chunk.

The fields of the data frame are the following
* voice_memo_name (without the .m4a ending, contains the time the memo was recorded)
* transcript_hash (SHA-256 hash of the full text transcript)
* offset (the start position in the transcript of the chunk)
* chunk_hash (SHA-256 hash of the chunk string)
* chunk_content (the string of the chunk)
* chunk_embedding (embedding vector of dimensinality 1536)

```
python3 embed_transcripts.py -i ./transcripts/ -o embeddings.json -api <open_ai_api_key>
```

The default chunk_size is 1500 and stride for chunk is 500. To change this, use parameters like this: ```-chunk 1000 -stride 300```