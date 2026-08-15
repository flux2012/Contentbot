"""
Step 5b: Publish the final video as an Instagram Reel using the Meta Graph API.

ONE-TIME SETUP (you do this once, manually):
1. Convert your Instagram account to a Business or Creator account (free, in the app)
2. Create a Facebook Page and link your Instagram account to it (free)
3. Go to https://developers.facebook.com/ -> create an App (type: Business)
4. Add the "Instagram Graph API" product
5. Generate a long-lived Page Access Token (Meta's docs walk through this:
   https://developers.facebook.com/docs/pages/access-tokens)
6. Get your Instagram Business Account ID (via Graph API Explorer)
7. Save both as GitHub Secrets: IG_ACCESS_TOKEN and IG_ACCOUNT_ID

NOTE: The video needs to be reachable at a public URL for Instagram to fetch it
(Instagram's API pulls the video from a link, it doesn't accept raw file upload).
This script uploads the final video to a temporary free file host (file.io) first,
then hands that link to Instagram. For a permanent solution you could instead
host clips in a public GitHub repo or free storage bucket.
"""

import os
import time
import requests

IG_ACCESS_TOKEN = os.environ["IG_ACCESS_TOKEN"]
IG_ACCOUNT_ID = os.environ["IG_ACCOUNT_ID"]

def upload_to_temp_host(file_path: str) -> str:
    with open(file_path, "rb") as f:
        r = requests.post("https://file.io", files={"file": f})
    r.raise_for_status()
    return r.json()["link"]

def main():
    import json
    with open("output/script.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    video_url = upload_to_temp_host("output/final_video.mp4")
    print(f"Video temporarily hosted at: {video_url}")

    # Step 1: create the media container
    create_url = f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/media"
    resp = requests.post(create_url, data={
        "media_type": "REELS",
        "video_url": video_url,
        "caption": data["caption"],
        "access_token": IG_ACCESS_TOKEN,
    })
    resp.raise_for_status()
    container_id = resp.json()["id"]

    # Step 2: poll until the container has finished processing
    status_url = f"https://graph.facebook.com/v19.0/{container_id}"
    for _ in range(30):
        status = requests.get(status_url, params={
            "fields": "status_code", "access_token": IG_ACCESS_TOKEN
        }).json()
        if status.get("status_code") == "FINISHED":
            break
        time.sleep(10)

    # Step 3: publish it
    publish_url = f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/media_publish"
    resp = requests.post(publish_url, data={
        "creation_id": container_id,
        "access_token": IG_ACCESS_TOKEN,
    })
    resp.raise_for_status()
    print(f"Published to Instagram: {resp.json()}")


if __name__ == "__main__":
    main()
