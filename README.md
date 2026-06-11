# Video Prompt Generator

A Streamlit app to convert textual prompts into images and short videos using free TTS and offline-friendly tools.

Try the demo (if deployed): https://video-prompt-generator-bzofecusaii79dpnxvadik.streamlit.app/

Quick start (local)

1. Clone:
   git clone https://github.com/infoshwetshivaprinting-cell/video-prompt-generator.git
2. Create a virtualenv and activate it:
   python -m venv .venv
   source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
3. Upgrade pip and install:
   python -m pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
4. (Optional) For offline TTS install dev deps:
   pip install -r dev-requirements.txt
5. Run locally:
   streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501

Notes
- The cloud deployment uses Streamlit Community Cloud and runtime.txt to request Python 3.11.
- Offline TTS (pyttsx3) is development-only and not installed on cloud hosts. See docs/TTS.md.

License
- MIT. See LICENSE file.
