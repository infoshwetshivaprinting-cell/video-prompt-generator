from typing import List


def create_video(image_files: List[str], audio_path: str, output_path: str, prompt: str = None):
    """Create a video (MP4) from image files and an audio file when possible.

    Falls back to creating an animated GIF (no audio) if moviepy or its
    dependencies (like imageio-ffmpeg or setuptools/pkg_resources) are missing
    in the environment. The function returns the path to the created asset
    (MP4 or GIF).
    """
    # Try to import moviepy lazily. If it fails due to missing runtime deps,
    # fall back to a GIF-only path that uses Pillow (which is more likely to be
    # available as a wheel).
    try:
        from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
        has_moviepy = True
    except Exception as e:
        has_moviepy = False
        moviepy_import_error = e

    if has_moviepy:
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

    # Fallback: create an animated GIF (no audio) using Pillow
    try:
        from PIL import Image
    except Exception as e:
        raise RuntimeError(
            "Neither moviepy nor Pillow are available in the environment. "
            "Cannot create video or GIF. Install the required packages and try again. "
            f"Original moviepy import error: {moviepy_import_error}; Pillow import error: {e}"
        )

    # Create GIF
    imgs = []
    for f in image_files:
        try:
            im = Image.open(f).convert('RGB')
            imgs.append(im)
        except Exception:
            # Skip images that cannot be opened
            continue

    if not imgs:
        raise RuntimeError("No images available to create GIF.")

    gif_path = output_path.rsplit('.', 1)[0] + '.gif'
    # duration in milliseconds per frame
    duration_ms = 2000
    imgs[0].save(gif_path, save_all=True, append_images=imgs[1:], duration=duration_ms, loop=0)

    # Note: audio is not included in GIF. If audio exists, keep the audio file as a separate download.
    return gif_path
