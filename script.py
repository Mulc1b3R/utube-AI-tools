import os
from openai import OpenAI

# 1. Initialize the client
# Tip: Using os.environ.get("OPENAI_API_KEY") is safer than hardcoding
client = OpenAI(api_key=" paste your api key here")

def generate_mega_script(topic):
    try:
        # PHASE 1: Data-Driven Outlining
        print(f"Phase 1: Researching and outlining {topic}...")
        outline_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a lead researcher. Create an exhaustive 10-point outline for a YouTube script. For every point, identify a specific data point, case study, or technical concept that MUST be explained."},
                {"role": "user", "content": f"Topic: {topic}"}
            ]
        )
        outline = outline_response.choices[0].message.content
        
        # PHASE 2: Comprehensive Scriptwriting
        print("Phase 2: Writing the deep-dive script (this may take a minute)...")
        full_script_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an elite YouTube scriptwriter. Using the provided outline, write a massive, high-retention script. Expand every section with maximum detail. Use a conversational, authoritative tone and include retention hooks between sections."},
                {"role": "user", "content": f"Outline to expand into a full script: {outline}"}
            ]
        )
        final_script = full_script_response.choices[0].message.content

        # 3. Save the research and script to a text file
        filename = "mega_youtube_script.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"TOPIC: {topic}\n\n--- RESEARCH OUTLINE ---\n{outline}\n\n--- COMPREHENSIVE SCRIPT ---\n{final_script}")
        
        print(f"Success! Your deep-dive script is ready in {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Allows you to type the topic directly into the terminal
    user_topic = input("Enter your video topic: ")
    generate_mega_script(user_topic)
