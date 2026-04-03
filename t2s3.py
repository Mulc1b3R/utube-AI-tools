import os
import datetime
from openai import OpenAI

# 1. Initialize the client
client = OpenAI(api_key="paste your api key here")

def split_text(text, limit=4000):
    """Splits long text into chunks at the nearest sentence end."""
    chunks = []
    while len(text) > limit:
        # Find the last period, exclamation, or question mark within the limit
        split_at = max(text.rfind('.', 0, limit), 
                       text.rfind('!', 0, limit), 
                       text.rfind('?', 0, limit))
        
        if split_at == -1:
            split_at = text.rfind(' ', 0, limit) # Fallback to space
            
        chunks.append(text[:split_at + 1].strip())
        text = text[split_at + 1:].strip()
    
    if text:
        chunks.append(text)
    return chunks

def generate_audio_from_file(file_path, voice="onyx"):
    try:
        # 2. Read the text file
        with open(file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()

        chunks = split_text(full_text)
        print(f"File loaded. Splitting into {len(chunks)} audio parts...")

        # 3. Process each chunk
        for i, chunk in enumerate(chunks):
            output_file = f"voiceover_part_{i+1}.mp3"
            print(f"Generating {output_file}...")
            
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=chunk
            )
            response.stream_to_file(output_file)

        print("\nSuccess! All audio parts are ready for CapCut.")

    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'. Make sure it's in the same folder.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Run the Script ---
if __name__ == "__main__":
    # Ensure you have a file named 'script.txt' in your folder!
    generate_audio_from_file("script.txt", voice="nova")
