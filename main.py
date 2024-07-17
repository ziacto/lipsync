import os
import json
import time
import requests

# Set your SyncLabs API key directly
syncLabsApiKey = "b955abe7-bab9-4dd4-b9e4-28d07ca48b8d"

# URLs for audio and video files on Supabase
audio_url = "https://vlcenhscwkvvvjnqypot.supabase.co/storage/v1/object/public/sample/hindi.mp3?t=2024-07-17T17%3A24%3A03.428Z"
video_url = "https://vlcenhscwkvvvjnqypot.supabase.co/storage/v1/object/public/sample/sample.mp4?t=2024-07-17T17%3A00%3A19.741Z"

def lip_sync(audio_url: str, video_url: str) -> str:
    """
    Perform lip sync using the SyncLabs API.
    """
    API_URL = "https://api.synclabs.so/lipsync"

    # Define the payload for the SyncLabs request
    payload = {
        "audioUrl": audio_url,
        "videoUrl": video_url,
        "synergize": True,
        "maxCredits": None,
        "webhookUrl": None,
        "model": "sync-1.6.0"
    }

    # Define the headers for the SyncLabs request
    headers = {
        "Content-Type": "application/json",
        "x-api-key": syncLabsApiKey,
        "accept": "application/json"
    }

    # Log sending request
    print('Sending request to SyncLabs at', API_URL)
    print('Payload:', json.dumps(payload, indent=2))

    # Make the POST request to SyncLabs
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

        # Log response received
        print('Response from SyncLabs received')

        # Check if the response is successful
        if response.status_code in [200, 201]:
            data = response.json()
            print('Response data:', json.dumps(data, indent=2))
            video_id = data.get("id")
            if not video_id:
                raise ValueError("No 'id' found in response")
        else:
            # Handle errors
            error_text = response.text
            print(f'Failed to lip sync video to audio: {response.status_code} {error_text}')
            return None
    except Exception as error:
        # Handle unexpected errors
        print(f'Unexpected error occurred: {error}')
        return None

    # Check the status of the job
    return check_job_status(video_id)

def check_job_status(video_id: str) -> str:
    """
    Check the status of the job using the SyncLabs API.
    """
    url = f'https://api.synclabs.so/lipsync/{video_id}'

    headers = {
        'accept': 'application/json',
        'x-api-key': syncLabsApiKey,
    }

    max_retries = 5
    retry_delay = 10  # seconds

    for attempt in range(max_retries):
        while True:
            # Make the GET request to check job status
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                status = data["status"]
                if status == "COMPLETED":
                    return data["videoUrl"]
                elif status == "FAILED":
                    print(f'Lip sync job failed: {data.get("errorMessage")}')
                    return None
                else:
                    print(f'Status: {status}. Waiting for completion...')
            else:
                print(f'Failed to get video details: {response.status_code}')
                print(response.text)
                return None

            # Wait before checking again
            time.sleep(10)
        print(f'Retrying ({attempt + 1}/{max_retries})...')
        time.sleep(retry_delay)
        retry_delay *= 2  # Exponential backoff

    print("Max retries reached. Lip sync process failed.")
    return None

def download_video(download_link: str, base_path: str, video_name: str) -> None:
    """
    Download the final video from the given URL.
    """
    # Send a HTTP request to the URL of the video
    r = requests.get(download_link, stream=True)

    # Open the file in write and binary mode
    with open(base_path + f"{video_name}_final_video.mp4", 'wb') as f:
        # Write the contents of the response (r.content) to a new file in binary mode.
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)

    print("Video downloaded successfully.")

def perform_lip_sync():
    """
    Perform the full lip sync process: lip sync, download result.
    """
    # Step 1: Perform lip sync using SyncLabs
    print("Performing lip sync using SyncLabs...")
    download_link = lip_sync(audio_url, video_url)

    if download_link:
        # Step 2: Download the final video
        print("Downloading the final video...")
        download_video(download_link, "./", "lip_synced_video")

        print("Lip sync process completed. Download link:", download_link)
    else:
        print("Lip sync process failed.")

if __name__ == '__main__':
    perform_lip_sync()
