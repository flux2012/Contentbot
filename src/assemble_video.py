"""
Step 4: Assemble images + voiceover + captions into one final vertical video.
"""

import json
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips
)

def main():
    with open("output/script.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("output/images/manifest.json", "r") as f:
        image_paths = json.load(f)

    audio = AudioFileClip("output/voice.mp3")
    total_duration = audio.duration
    per_image = total_duration / len(image_paths)

    clips = []
    for path in image_paths:
        clip = ImageClip(path).set_duration(per_image).resize(height=1920)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose").set_audio(audio)

    # Simple burned-in title text at the top
    title_clip = (
        TextClip(data["title"], fontsize=70, color="white", font="Arial-Bold",
                 size=(1000, None), method="caption")
        .set_position(("center", 100))
        .set_duration(total_duration)
    )

    final = CompositeVideoClip([video, title_clip])
    final.write_videofile("output/final_video.mp4", fps=30, codec="libx264",
                           audio_codec="aac")

    print("Final video saved to output/final_video.mp4")


if __name__ == "__main__":
    main()
