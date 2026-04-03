import os
import datetime
from openai import OpenAI

# 1. Initialize the client
client = OpenAI(api_key="paste your api key here")

# 2. Define the "Cast" outside the function
VOICE_MAP = {
    "NARRATOR": "onyx",
    "EXPERT": "nova",
    "GUEST": "shimmer"
}

def generate_multi_voice_audio(file_path):
    try:
        # Load your edited script
        with open(file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()
        
        lines = full_text.strip().split('\n')
        current_voice = "onyx" # Default voice
        
        print(f"Processing {len(lines)} lines for multi-voice output...")

        for i, line in enumerate(lines):
            line = line.strip()
            if not line: continue
            
            # --- LINE 41: Checking for Speaker Tags ---
            found_tag = False
            for tag, voice in VOICE_MAP.items():
                if line.upper().startswith(f"[{tag}]"):
                    current_voice = voice
                    # Remove the tag from the text actually spoken
                    line = line.replace(f"[{tag}]", "").replace(f"[{tag.lower()}]", "").strip()
                    found_tag = True
                    break
            
            # 3. Generate Audio for this line
            output_filename = f"part_{i+1}_{current_voice}.mp3"
            print(f"Generating: {output_filename}")
            
            response = client.audio.speech.create(
                model="tts-1",
                voice=current_voice,
                input=line
            )
            response.stream_to_file(output_filename)

        print("\nAll dialogue lines generated successfully!")

    except Exception as e:
        print(f"Error on processing: {e}")

if __name__ == "__main__":
    # Ensure you have a file named 'script.txt' formatted with [TAGS]
    generate_multi_voice_audio("script.txt")

