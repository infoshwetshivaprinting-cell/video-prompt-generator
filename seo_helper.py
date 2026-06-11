def generate_seo_metadata(prompt: str):
    title = prompt.strip().split('\n')[0][:60] if prompt else "Video"
    description = (prompt.strip()[:200] + '...') if prompt and len(prompt) > 200 else (prompt or "")
    keywords = ", ".join(list({w.strip().lower() for w in (prompt or '').split() if len(w) > 3})[:10])
    return {
        "title": title or "Video Prompt",
        "description": description,
        "keywords": keywords
    }
