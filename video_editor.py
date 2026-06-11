from typing import List


def create_video(image_files: List[str], audio_path: str, output_path: str, prompt: str = None):
    """Create a simple video from image files and an audio file.
    - Each image will be displayed for 2 seconds (adjustable).
    - The audio (if present) will be added as background.

    This function imports moviepy lazily and raises a clear error if moviepy or its
    binary dependencies are not available in the runtime. This avoids crashing the app at
    import time on hosts where moviepy dependencies are not yet installed.
    """
    try:
        # Import here to avoid import-time failures on hosts without moviepy/imageio-ffmpeg
        from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
    except Exception as e:
        # Provide a clear, actionable error message for the runtime logs
        raise RuntimeError(
            "moviepy (or one of its dependencies like imageio-ffmpeg or setuptools) is not available in the environment. "
            "Ensure requirements.txt includes moviepy, imageio, imageio-ffmpeg, setuptools and wheel, and your runtime supports ffmpeg. "
            f"Original error: {e}"
        )

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
