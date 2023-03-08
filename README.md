# transcribe voice memos
This Python script takes 3 inputs
* Input directory containing your voice memos. Find this directory by going to iTunes, sync with your iPhone, go to Voice memos, right click on a voice memo and click show in Finder.
* Output directory: If it does not exist it will be created for you. It will contain .txt files with the same names as the voice memo .m4a audio recording
* OpenAI api key: The voice memos are trancribed using OpenAI Whisper speech to text API. Go to platform. Sign up and get an API key at openai.com

# Usage
```
python3 transcribe_memos.py -i /Users/kasperrasmussen/Music/iTunes/iTunes\ Media/Voice\ Memos -o ./transcripts/ -api <open_ai_api_key>
```