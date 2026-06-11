import os
import streamlit as st
from config import OUTPUT_FOLDER
from voiceover_generator import generate_voiceover
from image_generator import create_images
from video_editor import create_video
from seo_helper import generate_seo_metadata
from logger import log_info, log_error

# Load local .env if present (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # python-dotenv not installed or .env not present — that's fine
    pass

st.set_page_config(page_title="Video Prompt Generator - Shorts", layout="centered")

st.title("Video Prompt Generator — YouTube Shorts")

prompt = st.text_area("Enter your video prompt", height=150)
num_images = st.number_input("Number of images", min_value=1, max_value=10, value=5)
preferred_tts = st.selectbox("TTS Provider (free options available)", ["gtts (free)", "pyttsx3 (offline, free)", "elevenlabs (paid)", "google (paid)"])

if st.button("Generate Short"):
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        audio_path = os.path.join(OUTPUT_FOLDER, "voiceover.mp3")
        try:
            with st.spinner("Generating voiceover..."):
                # Map UI selection to provider key
                provider_key = "gtts"
                if preferred_tts.startswith("pyttsx3"):
                    provider_key = "pyttsx3"
                elif preferred_tts.startswith("elevenlabs"):
                    provider_key = "elevenlabs"
                elif preferred_tts.startswith("google"):
                    provider_key = "google"

                # Use Streamlit secrets if available for providers (secure storage on Streamlit)
                provider_kwargs = {}
                if provider_key == "elevenlabs":
                    api_key = st.secrets.get("ELEVENLABS_API_KEY") if hasattr(st, "secrets") else os.getenv("ELEVENLABS_API_KEY")
                    voice_id = st.secrets.get("ELEVENLABS_VOICE_ID") if hasattr(st, "secrets") else os.getenv("ELEVENLABS_VOICE_ID")
                    if api_key:
                        os.environ["ELEVENLABS_API_KEY"] = api_key
                    if voice_id:
                        os.environ["ELEVENLABS_VOICE_ID"] = voice_id

                # Generate voiceover (defaults to free gTTS if no keys)
                generate_voiceover(prompt, audio_path, provider=provider_key)
            st.success("Voiceover generated")
            log_info("Voiceover generated")

            with st.spinner("Creating images..."):
                image_files = create_images(prompt, num_images, OUTPUT_FOLDER)
            st.success("Images created")
            log_info(f"Created {len(image_files)} images")

            output_video = os.path.join(OUTPUT_FOLDER, "short_generated.mp4")
            with st.spinner("Creating video (this may take a while)..."):
                create_video(image_files, audio_path, output_video, prompt)
            st.success("Video created")
            log_info(f"Video saved at {output_video}")

            # Show thumbnails
            st.subheader("Generated images")
            for img in image_files:
                st.image(img, use_column_width=True)

            # Show download button
            st.subheader("Download Video")
            with open(output_video, "rb") as f:
                video_bytes = f.read()
            st.download_button("Download the Short", data=video_bytes, file_name="short_generated.mp4", mime="video/mp4")

            # Show SEO metadata suggestions
            st.subheader("SEO Suggestions")
            meta = generate_seo_metadata(prompt)
            st.text_input("Title", value=meta["title"]) 
            st.text_area("Description", value=meta["description"], height=120)
            st.text_input("Keywords (comma-separated)", value=meta["keywords"]) 

        except Exception as e:
            st.error(f"An error occurred: {e}")
            log_error(str(e))
