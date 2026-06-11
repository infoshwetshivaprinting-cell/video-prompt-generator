from moviepy.editor import ImageSequenceClip, AudioFileClip

def create_video(image_files, audio_file, output_file):
    """Create a video by stitching images and adding audio."""
    clip = ImageSequenceClip(image_files, fps=1)
    audio = AudioFileClip(audio_file)
    clip = clip.set_audio(audio)
    clip.write_videofile(output_file, fps=24)

# Example of invoking video editing
if __name__ == "__main__":
    print("Creating a video out of generated assets.")
    create_video(["output/image_1.png", "output/image_2.png"], "output/voiceover.mp3", "output/demo_video.mp4")