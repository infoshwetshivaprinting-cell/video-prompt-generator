from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from typing import List


def create_video(image_files: List[str], audio_path: str, output_path: str, prompt: str = None):
    """Create a simple video from image files and an audio file.
    - Each image will be displayed for 2 seconds (adjustable).
    - The audio (if present) will be added as background.
    """
    duration_per_image = 2
    clips = []
    for img in image_files:
        clip = ImageClip(img).set_duration(duration_per_image)
        clips.append(clip)
    final = concatenate_videoclips(clips, method="compose")

    try:
        if audio_path and audio_path.strip():
            audio = AudioFileClip(audio_path)
            final = final.set_audio(audio)
    except Exception:
        # If audio fails to load, continue without audio
        pass

    # Write the video file
    final.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24, threads=2, verbose=False, logger=None)
    return output_path
