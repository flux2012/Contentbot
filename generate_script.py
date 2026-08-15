"""
Step 1: Generate a short video script using Google Gemini (free tier).

Get a free API key: https://aistudio.google.com/app/apikey
Set it as an environment variable / GitHub Secret named GEMINI_API_KEY
"""

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

NICHE = os.environ.get("CONTENT_NICHE", "short motivational life advice")

PROMPT = f"""
You are a viral short-form video scriptwriter for Instagram Reels and YouTube Shorts.

Write ONE short video script about: {NICHE}

Rules:
- Total spoken length: 30-45 seconds (about 90-120 words)
- Strong hook in the first line (first 3 seconds must grab attention)
- Simple, punchy, spoken language (not written/essay style)
- End with a short call to action (follow / comment / save)

Return ONLY valid JSON in this exact format, nothing else:
{{
  "title": "short catchy title for the video",
  "caption": "instagram/youtube caption with 3-5 relevant hashtags",
  "script": "the full spoken narration text, ready to be read aloud",
  "scene_prompts": ["image prompt 1 for scene 1", "image prompt 2 for scene 2", "image prompt 3 for scene 3"]
}}
"""

def main():
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(PROMPT)

    text = response.text.strip()
    # Clean up if the model wraps it in markdown code fences
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    data = json.loads(text)

    os.makedirs("output", exist_ok=True)
    with open("output/script.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Script generated:")
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
