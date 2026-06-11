import os
import streamlit as st
from config import OUTPUT_FOLDER
from voiceover_generator import generate_voiceover
from image_generator import create_images
from video_editor import create_video
from seo_helper import generate_seo_metadata
from logger import log_info, log_error

st.set_page_config(page_title="Video Prompt Generator - Shorts", layout="centered")

st.title("Video Prompt Generator — YouTube Shorts")

prompt = st.text_area("Enter your video prompt", height=150)
num_images = st.number_input("Number of images", min_value=1, max_value=10, value=5)

if st.button("Generate Short"):
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        audio_path = os.path.join(OUTPUT_FOLDER, "voiceover.mp3")
        try:
            with st.spinner("Generating voiceover..."):
                generate_voiceover(prompt, audio_path)
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
