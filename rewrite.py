import os
import datetime
from openai import OpenAI

# 1. Initialize the client
client = OpenAI(api_key="paste your api key here")

def split_text(text, limit=4000):
    """Splits long text into chunks for the 4,096 character TTS limit."""
    chunks = []
    while len(text) > limit:
        split_at = max(text.rfind('.', 0, limit), text.rfind('!', 0, limit), text.rfind('?', 0, limit))
        if split_at == -1: split_at = text.rfind(' ', 0, limit)
        chunks.append(text[:split_at + 1].strip())
        text = text[split_at + 1:].strip()
    if text: chunks.append(text)
    return chunks

def rewrite_and_generate_audio(transcript_file):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        output_txt = f"rewritten_script_{timestamp}.txt"

        # --- STEP 1: Rewrite the Transcript ---
        print(f"\n[1/3] Rewriting transcript: {transcript_file}...")
        with open(transcript_file, "r", encoding="utf-8") as f:
            raw_text = f.read()

        rewrite_res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional editor. Rewrite this transcript into a smooth, engaging YouTube narration. Remove filler words, fix grammar, and ensure it sounds natural for a voiceover."},
                {"role": "user", "content": f"Transcript to rewrite: {raw_text}"}
            ]
        )
        # Use choices[0] to avoid the 'list' error we saw earlier
        rewritten_text = rewrite_res.choices[0].message.content

        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(rewritten_text)

        # --- STEP 2: Human-in-the-loop Pause ---
        print("\n" + "="*50)
        print(f"PAUSED: Open '{output_txt}' and make your creative edits.")
        print("SAVE the file when you're finished.")
        print("="*50)
        input("\n>>> Press ENTER once you have saved your edits to generate the MP3...")

        # Reload your edited version
        with open(output_txt, "r", encoding="utf-8") as f:
            final_text = f.read()

        # --- STEP 3: Generate Audio ---
        print("\n[3/3] Generating Audio...")
        chunks = split_text(final_text)
        for i, chunk in enumerate(chunks):
            filename = f"narration_{timestamp}_part{i+1}.mp3"
            response = client.audio.speech.create(
                model="tts-1",
                voice="onyx", # Options: alloy, echo, fable, onyx, nova, shimmer
                input=chunk
            )
            response.stream_to_file(filename)
            print(f"   -> Saved {filename}")

        print("\nCOMPLETE! Your rewritten script and MP3s are ready.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ensure you have a file named 'raw_transcript.txt' ready
    rewrite_and_generate_audio("raw_transcript.txt")
