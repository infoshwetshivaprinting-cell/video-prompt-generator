from typing import List
import os
from pathlib import Path


def create_video(image_files: List[str], audio_path: str, output_path: str, prompt: str = None):
    """Create a video (MP4) from image files and an audio file when possible.

    Falls back to creating an animated GIF (no audio) if moviepy or its
    dependencies are missing in the environment. The function returns the path 
    to the created asset (MP4 or GIF).
    """
    try:
        from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
        has_moviepy = True
    except Exception as e:
        has_moviepy = False
        moviepy_import_error = str(e)

    if has_moviepy and image_files:
        try:
            duration_per_image = 2
            clips = []
            for img in image_files:
                if os.path.exists(img):
                    clip = ImageClip(img).set_duration(duration_per_image)
                    clips.append(clip)
            
            if not clips:
                raise RuntimeError("No valid images found for video creation.")
            
            final = concatenate_videoclips(clips, method="compose")

            # Attach audio if available
            if audio_path and os.path.exists(audio_path):
                try:
                    audio = AudioFileClip(audio_path)
                    final = final.set_audio(audio)
                except Exception as audio_error:
                    # Continue without audio if loading fails
                    pass

            # Write the video file with safe parameters
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            final.write_videofile(
                output_path, 
                codec='libx264', 
                audio_codec='aac', 
                fps=24, 
                verbose=False, 
                logger=None,
                preset='medium'
            )
            final.close()
            return output_path
        except Exception as e:
            # If moviepy fails, fall back to GIF
            pass

    # Fallback: create an animated GIF (no audio) using Pillow
    try:
        from PIL import Image
    except Exception as e:
        raise RuntimeError(
            f"Neither moviepy nor Pillow are available. Cannot create video or GIF. Error: {e}"
        )

    imgs = []
    for f in image_files:
        if os.path.exists(f):
            try:
                im = Image.open(f).convert('RGB')
                imgs.append(im)
            except Exception:
                continue

    if not imgs:
        raise RuntimeError("No valid images available to create GIF.")

    gif_path = output_path.rsplit('.', 1)[0] + '.gif'
    os.makedirs(os.path.dirname(gif_path) or ".", exist_ok=True)
    
    duration_ms = 2000
    imgs[0].save(gif_path, save_all=True, append_images=imgs[1:], duration=duration_ms, loop=0)
    return gif_path
