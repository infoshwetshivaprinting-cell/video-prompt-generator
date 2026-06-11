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

            default_output = os.path.join(OUTPUT_FOLDER, "short_generated.mp4")
            created_path = None
            with st.spinner("Creating video (this may take a while)..."):
                try:
                    created_path = create_video(image_files, audio_path, default_output, prompt)
                except Exception as e:
                    # Log and keep going to handle fallback or show error to user
                    log_error(f"create_video raised an exception: {e}")
                    created_path = None

            output_video = created_path if created_path else default_output
            if not os.path.exists(output_video):
                # If the expected output doesn't exist, try to find any generated file in OUTPUT_FOLDER
                candidates = [os.path.join(OUTPUT_FOLDER, f) for f in os.listdir(OUTPUT_FOLDER)]
                candidates = [c for c in candidates if os.path.isfile(c) and os.path.getsize(c) > 0]
                # Prefer .mp4, then .gif
                mp4s = [c for c in candidates if c.lower().endswith('.mp4')]
                gifs = [c for c in candidates if c.lower().endswith('.gif')]
                if mp4s:
                    output_video = sorted(mp4s, key=os.path.getmtime)[-1]
                elif gifs:
                    output_video = sorted(gifs, key=os.path.getmtime)[-1]

            if not os.path.exists(output_video):
                st.error("Video creation failed — output file not found.")
                log_error(f"Expected output not found: {output_video}")
            else:
                st.success("Video created")
                log_info(f"Video saved at {output_video}")

                # Display the created media inline
                filename = os.path.basename(output_video)
                if filename.lower().endswith('.gif'):
                    try:
                        st.image(output_video, caption=filename, use_column_width=True)
                    except Exception:
                        pass
                else:
                    try:
                        st.video(output_video)
                    except Exception:
                        pass

                # Prepare download
                try:
                    with open(output_video, "rb") as f:
                        media_bytes = f.read()
                    mime = "video/mp4" if filename.lower().endswith('.mp4') else ("image/gif" if filename.lower().endswith('.gif') else "application/octet-stream")
                    st.download_button(f"Download the Short ({filename})", data=media_bytes, file_name=filename, mime=mime)
                except Exception as e:
                    st.error(f"Could not prepare download: {e}")
                    log_error(f"Download preparation failed: {e}")

                # Show SEO metadata suggestions
                st.subheader("SEO Suggestions")
                meta = generate_seo_metadata(prompt)
                st.text_input("Title", value=meta["title"]) 
                st.text_area("Description", value=meta["description"], height=120)
                st.text_input("Keywords (comma-separated)", value=meta["keywords"]) 

        except Exception as e:
            st.error(f"An error occurred: {e}")
            log_error(str(e))
