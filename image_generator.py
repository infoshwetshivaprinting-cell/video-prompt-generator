"""image_generator.py

Generate images for video prompts using Automatic1111 WebUI when available.
Falls back to a simple placeholder image generator using Pillow if the API is
not reachable. Saves images to the output folder and returns a list of paths.
"""
from typing import List
import os
import base64
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Config: allow overriding the Automatic1111 URL via environment or Streamlit secrets
AUTOMATIC1111_URL = os.environ.get("AUTOMATIC1111_URL", "http://127.0.0.1:7860")


def _save_base64_image(b64str: str, path: str) -> None:
    data = base64.b64decode(b64str)
    img = Image.open(BytesIO(data)).convert("RGB")
    img.save(path, format="JPEG", quality=90)

def _placeholder_create_images(prompt: str, num_images: int, output_folder: str) -> List[str]:
    """Create simple placeholder images that contain the prompt text."""
    os.makedirs(output_folder, exist_ok=True)
    files = []
    width, height = 1920, 1080

    for i in range(num_images):
        img = Image.new("RGB", (width, height), color=(73, 109, 137))
        draw = ImageDraw.Draw(img)

        text = f"{prompt[:200]}\n\nImage {i+1}/{num_images}"

        # Load font with fallback
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        except Exception:
            font = ImageFont.load_default()

        # Calculate text bbox and center it
        try:
            bbox = draw.multiline_textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except Exception:
            # Older Pillow fallback
            text_w, text_h = draw.textsize(text, font=font)

        x = (width - text_w) / 2
        y = (height - text_h) / 2

        draw.multiline_text((x, y), text, fill=(255, 255, 255), font=font, align="center")

        path = os.path.join(output_folder, f"image_{i+1}.jpg")
        img.save(path, format="JPEG", quality=85)
        files.append(path)

    return files


def create_images_auto1111(prompt: str, num_images: int, output_folder: str,
                           width: int = 1920, height: int = 1080,
                           steps: int = 28, cfg_scale: float = 9.0,
                           sampler: str = "DPM++ 2M Karras",
                           negative_prompt: str = "") -> List[str]:
    """
    Generate images using the Automatic1111 WebUI API (/sdapi/v1/txt2img).
    Falls back to placeholder images if the API request fails.
    """
    os.makedirs(output_folder, exist_ok=True)
    api = AUTOMATIC1111_URL.rstrip("/") + "/sdapi/v1/txt2img"
    files: List[str] = []

    for i in range(num_images):
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "sampler_index": sampler,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "batch_size": 1,
        }
        try:
            resp = requests.post(api, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            images_b64 = data.get("images", [])
            if not images_b64:
                raise RuntimeError("No images returned from Automatic1111")
            out_path = os.path.join(output_folder, f"image_{i+1}.jpg")
            _save_base64_image(images_b64[0], out_path)
            files.append(out_path)
        except Exception as e:
            print(f"[image_generator] Automatic1111 generation failed: {e} - falling back to placeholders")
            remaining = num_images - len(files)
            placeholder = _placeholder_create_images(prompt, remaining, output_folder)
            files.extend(placeholder)
            break

    return files


def create_images(prompt: str, num_images: int, output_folder: str) -> List[str]:
    """High-level image creation entrypoint used by the app.

    Tries Automatic1111 first (if reachable via AUTOMATIC1111_URL), otherwise
    falls back to placeholder images so the application remains functional.
    """
    # Quick health check for Automatic1111
    try:
        ping = requests.get(AUTOMATIC1111_URL.rstrip("/") + "/sdapi/v1/version", timeout=5)
        if ping.ok:
            return create_images_auto1111(prompt, num_images, output_folder)
    except Exception:
        pass

    return _placeholder_create_images(prompt, num_images, output_folder)
