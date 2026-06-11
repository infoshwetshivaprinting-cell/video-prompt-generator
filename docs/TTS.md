Free TTS and deployment options

This document explains free alternatives for TTS and how to use them in this project. The goal is to allow you to create videos and images without requiring paid services.

1) gTTS (Google Translate TTS) — free
- Pros: Simple, free, no API key required.
- Cons: Voice quality is basic; rate limits may apply.
- Usage: This is the default provider in the app. No keys required.

2) pyttsx3 — offline TTS (free)
- Pros: Runs locally without internet; fully free.
- Cons: Voices depend on OS; requires platform TTS engines.
- Usage: Select "pyttsx3 (offline, free)" in the Streamlit UI. It will synthesize audio locally and save to an MP3.

3) Coqui TTS / Mozilla TTS — open-source (free)
- Pros: High-quality open-source models available.
- Cons: Requires setup and model downloads; may need GPU for best performance.
- Usage: Not provided out-of-the-box in this repo, but you can integrate by adding a provider in `tts_providers.py` that calls Coqui inference.

Paid providers (optional)
- ElevenLabs and Google Cloud TTS are supported as optional providers in the code, but they require API keys and may incur costs. The app defaults to free providers when keys are not set.

How to pick a provider
- For a fully free setup, use pyttsx3 (offline) or gTTS (online free). Both are included in requirements.
- If you later want higher-quality voices, you can add an API key to your environment or use Streamlit secrets for deployment.
