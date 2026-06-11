Free TTS and deployment options

This document explains free alternatives for TTS and how to use them in this project. The goal is to allow you to create videos and images without requiring paid services.

Important change: pyttsx3 is now a development-only dependency and is not installed automatically on cloud hosts (like Streamlit Community Cloud). Install it locally if you want offline TTS during development.

1) gTTS (Google Translate TTS) — free
- Pros: Simple, free, no API key required.
- Cons: Voice quality is basic; rate limits may apply.
- Usage: This is the default provider in the app. No keys required.

2) pyttsx3 — offline TTS (free, local only)
- Pros: Runs locally without internet; fully free.
- Cons: Voices depend on OS; requires platform TTS engines (espeak on Linux).
- Installation (local development):
  - pip install -r dev-requirements.txt
  - On Debian/Ubuntu you may need: sudo apt-get install espeak libespeak1
  - On macOS/Windows system voices are typically available by default.

3) Coqui TTS / Mozilla TTS — open-source (free)
- Pros: High-quality open-source models available.
- Cons: Requires setup and model downloads; may need GPU for best performance.
- Usage: Not provided out-of-the-box in this repo, but you can integrate by adding a provider in `tts_providers.py` that calls Coqui inference.

Paid providers (optional)
- ElevenLabs and Google Cloud TTS are supported as optional providers in the code, but they require API keys and may incur costs. The app defaults to free providers when keys are not set.

How to pick a provider
- For a fully free setup on a hosted platform, use gTTS (online free). For local offline use, install pyttsx3 via dev-requirements.
- The cloud deployment uses `requirements.txt` and will not attempt to install pyttsx3.
