import os
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip
from PIL import Image

def generate_voiceover(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)

def create_images(prompt, num_images, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    images = []
    for i in range(num_images):
        file_path = os.path.join(output_folder, f"image_{i+1}.png")
        img = Image.new('RGB', (1280, 720), color=(73, 109, 173))
        img.save(file_path)
        images.append(file_path)
    return images

def create_video(image_files, audio_file, output_file):
    clip = ImageSequenceClip(image_files, fps=1)
    audio = AudioFileClip(audio_file)
    clip = clip.set_audio(audio)
    clip.write_videofile(output_file, fps=24)

def main():
    prompt = input("Enter your video prompt: ")
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    audio_file = os.path.join(output_folder, "voiceover.mp3")

    print("Generating voiceover...")
    generate_voiceover(prompt, audio_file)

    print("Creating images...")
    image_files = create_images(prompt, num_images=5, output_folder=output_folder)

    print("Creating video...")
    output_video = os.path.join(output_folder, "generated_video.mp4")
    create_video(image_files, audio_file, output_video)

    print(f"Video saved at: {output_video}")

if __name__ == "__main__":
    main()