from PIL import Image, ImageDraw, ImageFont
import os
from typing import List

def create_images(prompt: str, num_images: int, output_folder: str) -> List[str]:
    """Create placeholder images based on the prompt.
    
    Generates images in 16:9 landscape format (1920x1080) by default.
    Returns a list of file paths.
    """
    os.makedirs(output_folder, exist_ok=True)
    files = []
    
    # 16:9 landscape format (can be adjusted based on template)
    width, height = 1920, 1080
    
    for i in range(num_images):
        img = Image.new('RGB', (width, height), color=(73, 109, 137))
        draw = ImageDraw.Draw(img)
        
        # Prepare text
        text = f"{prompt[:60]}...\nImage {i+1}/{num_images}"
        
        # Load font with fallback
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        except Exception:
            font = ImageFont.load_default()
        
        # Use textbbox for modern Pillow compatibility
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        # Center the text
        x = (width - text_w) / 2
        y = (height - text_h) / 2
        
        draw.multiline_text((x, y), text, fill=(255, 255, 255), font=font, align='center')
        
        path = os.path.join(output_folder, f"image_{i+1}.jpg")
        img.save(path, format='JPEG', quality=85)
        files.append(path)
    
    return files
