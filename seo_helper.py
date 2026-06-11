import os

def generate_seo_metadata(prompt):
    """Generate SEO metadata for YouTube Shorts."""
    keywords = [word for word in prompt.split() if len(word) > 3]
    title = f"{prompt[:50]}..." if len(prompt) > 50 else prompt
    description = f"This is a YouTube Short created from the prompt: {prompt}"

    return {
        "title": title,
        "description": description,
        "keywords": ", ".join(keywords)
    }

# Example usage
if __name__ == "__main__":
    prompt = "Create engaging YouTube Shorts with Open Source Tools!"
    metadata = generate_seo_metadata(prompt)
    print("Generated Metadata:")
    print(metadata)