"""Simple wrapper that exposes generate_voiceover used by the Streamlit app.

This module delegates to tts_providers.generate_voiceover. Keeping this wrapper allows
existing code that imports `voiceover_generator.generate_voiceover` to continue working.
"""
from tts_providers import generate_voiceover as _generate


def generate_voiceover(prompt: str, output_path: str, provider: str = None, **kwargs):
    return _generate(prompt, output_path, provider=provider, **kwargs)
