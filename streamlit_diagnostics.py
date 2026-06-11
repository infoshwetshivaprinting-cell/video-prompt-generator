"""
Streamlit diagnostic tool for testing video generation.
Add this to your Streamlit app sidebar for real-time diagnostics.
"""

import streamlit as st
import os
import sys
from pathlib import Path

def show_diagnostics():
    """Display diagnostic information about video generation setup."""
    
    with st.sidebar.expander("?? Video Generation Diagnostics", expanded=False):
        st.write("### System Information")
        st.write(f"**Python Version:** {sys.version}")
        st.write(f"**Platform:** {sys.platform}")
        
        st.write("### Dependency Check")
        
        deps_status = {}
        
        # MoviePy
        try:
            from moviepy.editor import ImageClip, concatenate_videoclips
            import moviepy
            deps_status['MoviePy'] = f"? {moviepy.__version__}"
        except ImportError as e:
            deps_status['MoviePy'] = f"? {str(e)[:50]}"
        
        # PIL
        try:
            from PIL import Image
            import PIL
            deps_status['PIL'] = f"? {PIL.__version__}"
        except ImportError as e:
            deps_status['PIL'] = f"? {str(e)[:50]}"
        
        # gTTS
        try:
            from gtts import gTTS
            deps_status['gTTS'] = "? Available"
        except ImportError as e:
            deps_status['gTTS'] = f"? {str(e)[:50]}"
        
        # imageio
        try:
            import imageio
            deps_status['imageio'] = f"? {imageio.__version__}"
        except ImportError as e:
            deps_status['imageio'] = f"? {str(e)[:50]}"
        
        for dep, status in deps_status.items():
            st.write(f"- **{dep}**: {status}")
        
        st.write("### Output Folder")
        try:
            output_folder = "output"
            if os.path.exists(output_folder):
                files = os.listdir(output_folder)
                st.write(f"**Contents:** {len(files)} items")
                if files:
                    for f in sorted(files):
                        path = os.path.join(output_folder, f)
                        if os.path.isfile(path):
                            size_kb = os.path.getsize(path) / 1024
                            st.write(f"  - {f} ({size_kb:.1f} KB)")
                        else:
                            st.write(f"  - {f}/ (directory)")
            else:
                st.write("**Status:** Not created yet")
        except Exception as e:
            st.write(f"**Error:** {e}")
        
        st.write("### Quick Test")
        if st.button("Test Image Creation"):
            try:
                from image_generator import create_images
                test_images = create_images("Test", 2, "test_diag_output")
                st.success(f"? Created {len(test_images)} test images")
                for img in test_images:
                    if os.path.exists(img):
                        st.write(f"  - {os.path.basename(img)}")
            except Exception as e:
                st.error(f"? Failed: {e}")
        
        if st.button("Test GIF Creation"):
            try:
                from image_generator import create_images
                from video_editor import create_video
                test_images = create_images("Test", 2, "test_diag_output")
                result = create_video(test_images, "", "test_diag_output/test.mp4")
                st.success(f"? Created: {os.path.basename(result)}")
                st.write(f"  Size: {os.path.getsize(result) / 1024:.1f} KB")
            except Exception as e:
                st.error(f"? Failed: {e}")

if __name__ == "__main__":
    show_diagnostics()
