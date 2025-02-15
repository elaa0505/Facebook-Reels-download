import requests
import json
import os

# Author: Elango Saminathan
# Email : elaaisolution@gmail.com


# File containing list of URLs (one per line)
TEXT_FILE = "reel_links.txt"

# Output folder for downloaded videos
OUTPUT_FOLDER = "OutPath"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# API endpoint
API_URL = "https://contentstudio.io/.netlify/functions/facebookdownloaderapi"

# Read URLs from file
with open(TEXT_FILE, "r") as file:
    links = file.readlines()

# Loop through each link and process
i = 1
for link in links:
    i += 1
    print(i)
    link = link.strip()  # Remove newline characters
    if not link:
        continue  # Skip empty lines

    # Create the JSON payload
    payload = json.dumps({"url": link})
    #print(payload)
    # Send POST request
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, data=payload, headers=headers)
    #print(response.json())

    # Check response
    if response:
        try:
            json_data = response.json()
            video_url = json_data.get("url")  # Adjust key based on actual API response
            

            if video_url:
                print(f"✅ Video Found: {video_url}")
                
                

                # Download video
                video_response = requests.get(video_url, stream=True)
                video_filename = os.path.join(OUTPUT_FOLDER, f"{link.split('/')[-1]}{i}.mp4")
                

                with open(video_filename, "wb") as video_file:
                    for chunk in video_response.iter_content(chunk_size=1024):
                        video_file.write(chunk)

                print(f"📥 Downloaded: {video_filename}")
            else:
                print("❌ Video URL not found in response")

        except json.JSONDecodeError:
            print("❌ Invalid JSON response")
    else:
        print(f"❌ API Error: {response.status_code} - {response.text}")
