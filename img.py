import os
import requests
import datetime
from openai import OpenAI

# 1. Initialize the client
client = OpenAI(api_key="paste your api key here")

def generate_and_download_image(prompt, filename_base="thumbnail"):
    try:
        print(f"Generating image for: {prompt}...")
        
        # 2. Request image from DALL-E 3 (Widescreen for YouTube)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",  # Optimal YouTube thumbnail size
            quality="standard",
            n=1,
        )

        # Access the URL from the response
        image_url = response.data[0].url
        
        # 3. Download the image file locally
        print("Downloading image...")
        img_data = requests.get(image_url).content
        
        # Create a unique filename with a timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"{filename_base}_{timestamp}.png"
        
        # Save to the current folder
        with open(filename, 'wb') as handler:
            handler.write(img_data)
            
        print(f"Success! Your thumbnail is saved as: {filename}")
        return filename

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    user_prompt = input("Enter your thumbnail description: ")
    generate_and_download_image(user_prompt)
