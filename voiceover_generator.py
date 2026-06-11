from tts_providers import generate_voiceover as tts_generate

def generate_voiceover(prompt: str, output_path: str, provider: str = None, **kwargs):
    """Wrapper around tts_providers.generate_voiceover.
    Keeps a stable interface for streamlit_app.py.
    """
    return tts_generate(prompt, output_path, provider=provider, **kwargs)
