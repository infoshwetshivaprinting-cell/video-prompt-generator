# Video Prompt Generator — YouTube Shorts

This repository provides tools to generate short vertical videos (YouTube Shorts) from text prompts. It includes components for generating voiceovers, creating vertical images, composing videos, and a Streamlit web UI to run everything from a browser.

## What's included

- streamlit_app.py — Browser UI (Streamlit) to generate Shorts
- image_generator.py — Creates 9:16 images from prompts
- video_editor.py — Composes images and audio into a vertical video
- seo_helper.py — Generates title/description/keywords suggestions
- logger.py — Simple logging utility
- requirements.txt — Python dependencies
- test_logger.py — Unit tests for the logger

## Quickstart (local)

1. Clone the repo:
   git clone https://github.com/infoshwetshivaprinting-cell/video-prompt-generator.git
   cd video-prompt-generator

2. Create a virtual environment and install dependencies:
   python -m venv .venv

   # macOS / Linux
   source .venv/bin/activate

   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1

   pip install -r requirements.txt

3. Run the Streamlit app:
   streamlit run streamlit_app.py

4. Open the URL shown by Streamlit in your browser. Use the UI to enter a prompt, generate images, voiceover, and the Short.

## Deploy to Streamlit Community Cloud

1. Make the repository public (Settings → General → Change repository visibility → Make public) and ensure there are no secrets in the repo.
2. Sign in to https://share.streamlit.io with your GitHub account.
3. Click "New app" → select this repository, the `main` branch, and `streamlit_app.py` as the main file → Deploy.

Streamlit will install dependencies from `requirements.txt` and deploy the app.

## Tests / CI

A GitHub Actions workflow is included to run unit tests (`pytest`) on push and pull requests. Tests can also be run locally with:

    python -m pytest -q

## Security & Notes

- Do NOT commit API keys or other secrets. Use environment variables or GitHub secrets for deployments that require credentials.
- MoviePy can be CPU-intensive. For production or high-volume use, consider offloading encoding to a more capable environment.

## License

Add your preferred license file (e.g., MIT LICENSE) if you plan to make this repo public.
