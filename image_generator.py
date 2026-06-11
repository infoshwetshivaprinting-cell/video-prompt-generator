from PIL import Image, ImageDraw, ImageFont
import os
from typing import List

def create_images(prompt: str, num_images: int, output_folder: str) -> List[str]:
    """Create simple placeholder images based on the prompt.
    Returns a list of file paths.
    """
    os.makedirs(output_folder, exist_ok=True)
    files = []
    width, height = 720, 1280
    for i in range(num_images):
        img = Image.new('RGB', (width, height), color=(73, 109, 137))
        draw = ImageDraw.Draw(img)
        text = f"{prompt[:60]}...\nImage {i+1}"
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        except Exception:
            font = ImageFont.load_default()
        text_w, text_h = draw.multiline_textsize(text, font=font)
        draw.multiline_text(((width-text_w)/2, (height-text_h)/2), text, fill=(255,255,255), font=font, align='center')
        path = os.path.join(output_folder, f"image_{i+1}.jpg")
        img.save(path, format='JPEG', quality=85)
        files.append(path)
    return files
