"""Simple CLI entrypoint for generating a short video from a text prompt.

This script is primarily for local testing and mirrors what the Streamlit
app does: generate a voiceover, create images from a prompt, and assemble
those images (with optional audio) into an MP4 or GIF.
"""
import os
from gtts import gTTS
from image_generator import create_images
from video_editor import create_video

def generate_voiceover(text: str, output_file: str) -> None:
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)

def main():
    prompt = input("Enter your video prompt: ").strip()
    if not prompt:
        print("No prompt provided. Exiting.")
        return

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    audio_file = os.path.join(output_folder, "voiceover.mp3")

    print("Generating voiceover...")
    generate_voiceover(prompt, audio_file)

    print("Creating images...")
    image_files = create_images(prompt, num_images=5, output_folder=output_folder)
    print(f"Created {len(image_files)} images: {image_files}")

    print("Creating video...")
    output_video = os.path.join(output_folder, "generated_video.mp4")
    result = create_video(image_files, audio_file, output_video)
    print(f"Result saved at: {result}")

if __name__ == '__main__':
    main()
