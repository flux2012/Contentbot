"""
Step 3: Generate voiceover narration using edge-tts (100% free, no API key).

Voice options: https://github.com/rany2/edge-tts (run `edge-tts --list-voices`)
Good Hindi/English voices: "en-US-GuyNeural", "en-IN-PrabhatNeural", "hi-IN-MadhurNeural"
"""

import asyncio
import json
import os
import edge_tts

VOICE = os.environ.get("TTS_VOICE", "en-US-GuyNeural")

async def main():
    with open("output/script.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs("output", exist_ok=True)
    out_path = "output/voice.mp3"

    communicate = edge_tts.Communicate(data["script"], VOICE)
    await communicate.save(out_path)
    print(f"Voiceover saved to {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
