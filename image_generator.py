import os
from PIL import Image

def create_images(prompt, num_images, output_folder):
    """Generate placeholder images based on a text prompt."""
    os.makedirs(output_folder, exist_ok=True)
    images = []
    for i in range(num_images):
        file_path = os.path.join(output_folder, f"image_{i+1}.png")
        img = Image.new('RGB', (1280, 720), color=(73, 109, 173))
        img.save(file_path)
        images.append(file_path)
    return images

# Example usage
if __name__ == "__main__":
    create_images("Sample prompt", 5, "output")