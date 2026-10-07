"""
Step 5a: Upload the final video to YouTube as a Short.

ONE-TIME SETUP (you do this once, manually):
1. Go to https://console.cloud.google.com/ -> create a project
2. Enable "YouTube Data API v3"
3. Create OAuth 2.0 credentials (Desktop App type) -> download client_secret.json
4. Run `python src/get_youtube_token.py` locally ONCE to generate token.json
   (this opens a browser for you to log into YOUR YouTube channel and approve it)
5. Save the contents of token.json as a GitHub Secret named YOUTUBE_TOKEN_JSON
   Save the contents of client_secret.json as a GitHub Secret named YOUTUBE_CLIENT_SECRET

After that, this script runs fully unattended.
"""

import json
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_authenticated_service():
    token_data = json.loads(os.environ["YOUTUBE_TOKEN_JSON"])
    creds = Credentials.from_authorized_user_info(token_data)
    return build("youtube", "v3", credentials=creds)

def main():
    with open("output/script.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": data["title"][:100],
            "description": data["caption"],
            "tags": ["shorts"],
            "categoryId": "22",
        },
        "status": {"privacyStatus": "public"},
    }

    media = MediaFileUpload("output/final_video.mp4", chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    print(f"Uploaded to YouTube: https://youtube.com/watch?v={response['id']}")


if __name__ == "__main__":
    main()
