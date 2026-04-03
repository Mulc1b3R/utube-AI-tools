from icrawler.builtin import BingImageCrawler # Changed from Google to Bing
import os

def download_images(keyword, count):
    # 1. Create a clean folder name
    folder_name = keyword.replace(" ", "_").lower()
    
    # 2. Use BingImageCrawler (much more stable than Google)
    crawler = BingImageCrawler(storage={'root_dir': folder_name})
    
    print(f"Searching for '{keyword}' and downloading {count} images...")
    
    # 3. Start the crawl
    # We add a filter for 'large' to ensure high-quality YouTube b-roll
    crawler.crawl(keyword=keyword, max_num=count, filters=dict(size='large'))
    
    print(f"\nDone! Check the '{folder_name}' folder.")

if __name__ == "__main__":
    search_term = input("Enter search keyword: ")
    num_images = int(input("How many images? "))
    download_images(search_term, num_images)
