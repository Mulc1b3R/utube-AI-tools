import os
from openai import OpenAI

# 1. Initialize the client
client = OpenAI(api_key="paste your api key here")

def transcribe_audio(file_path):
    try:
        print(f"Transcribing {file_path}... this may take a moment.")
        
        # 2. Open the audio file
        with open(file_path, "rb") as audio_file:
            # 3. Call the Whisper API
            # Whisper-1 is the current state-of-the-art model for this task
            transcript_res = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text" # Returns plain text instead of JSON
            )
        
        # 4. Save to a text file
        output_filename = "transcript.txt"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(transcript_res)
            
        print(f"Success! Transcript saved to {output_filename}")
        return transcript_res

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Change 'audio_part_1.mp3' to your actual file name
    transcribe_audio("input.mp3")
