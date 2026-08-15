"""
Step 2: Generate AI images for each scene using Pollinations.ai (free, no API key needed).
"""

import json
import os
import urllib.parse
import requests

def generate_image(prompt: str, out_path: str, width=1080, height=1920):
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&nologo=true"
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)


def main():
    with open("output/script.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs("output/images", exist_ok=True)
    image_paths = []
    for i, prompt in enumerate(data["scene_prompts"]):
        out_path = f"output/images/scene_{i}.jpg"
        print(f"Generating image {i+1}/{len(data['scene_prompts'])}: {prompt}")
        generate_image(prompt, out_path)
        image_paths.append(out_path)

    with open("output/images/manifest.json", "w") as f:
        json.dump(image_paths, f, indent=2)

    print("All images generated.")


if __name__ == "__main__":
    main()
