import os
from PIL import Image, ImageDraw, ImageFont

def create_images(prompt, num_images, output_folder):
    """Generate placeholder images for YouTube Shorts with 9:16 aspect ratio."""
    os.makedirs(output_folder, exist_ok=True)
    images = []
    for i in range(num_images):
        file_path = os.path.join(output_folder, f"image_{i+1}.png")
        img = Image.new('RGB', (1080, 1920), color=(73, 109, 173))  # 9:16 aspect ratio
        draw = ImageDraw.Draw(img)

        # Add prompt text to the image (centered)
        font_size = 48
        font = ImageFont.load_default()  # Load default font
        text_width, text_height = draw.textsize(prompt, font=font)
        text_x = (img.width - text_width) // 2
        text_y = (img.height - text_height) // 2
        draw.text((text_x, text_y), prompt, fill="white", font=font)

        img.save(file_path)
        images.append(file_path)
    return images

# Example usage
if __name__ == "__main__":
    create_images("Sample prompt", 5, "output")