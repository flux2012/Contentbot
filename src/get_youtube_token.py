"""
RUN THIS ONCE ON YOUR OWN COMPUTER (not on GitHub Actions).
It opens a browser, you log into your YouTube channel, approve access,
and it saves token.json which you then copy into a GitHub Secret.

Usage:
    python src/get_youtube_token.py
"""

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)

    with open("token.json", "w") as f:
        f.write(creds.to_json())

    print("Saved token.json - copy its full contents into a GitHub Secret named YOUTUBE_TOKEN_JSON")


if __name__ == "__main__":
    main()
