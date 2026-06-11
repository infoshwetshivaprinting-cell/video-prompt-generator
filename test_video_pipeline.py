#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script for video generation pipeline.
Run locally before deploying to Streamlit Cloud: python test_video_pipeline.py
"""

import os
import sys
import tempfile
from pathlib import Path

def test_dependencies():
    """Test that all required dependencies are available."""
    print("\n=== Testing Dependencies ===")
    
    dependencies = {
        'PIL': 'Pillow',
        'moviepy': 'MoviePy',
        'gtts': 'gTTS',
        'imageio': 'imageio',
        'streamlit': 'Streamlit',
    }
    
    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"[OK] {name}")
        except ImportError as e:
            print(f"[FAIL] {name}: {e}")
            all_ok = False
    
    return all_ok

def test_image_creation():
    """Test image creation functionality."""
    print("\n=== Testing Image Creation ===")
    
    try:
        from image_generator import create_images
        with tempfile.TemporaryDirectory() as tmpdir:
            images = create_images("Test prompt for video", num_images=3, output_folder=tmpdir)
            if len(images) == 3 and all(os.path.exists(f) for f in images):
                print(f"[OK] Created 3 images: {[os.path.basename(f) for f in images]}")
                return True
            else:
                print("[FAIL] Image creation did not produce expected files")
                return False
    except Exception as e:
        print(f"[FAIL] Image creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gif_creation():
    """Test GIF creation (fallback mechanism)."""
    print("\n=== Testing GIF Creation (Fallback) ===")
    
    try:
        from image_generator import create_images
        from video_editor import create_video
        
        with tempfile.TemporaryDirectory() as tmpdir:
            images = create_images("GIF test", num_images=3, output_folder=tmpdir)
            output_path = os.path.join(tmpdir, "test.mp4")
            
            # Force GIF creation by not importing moviepy
            result = create_video(images, "", output_path)
            
            if result.endswith('.gif') and os.path.exists(result):
                size_kb = os.path.getsize(result) / 1024
                print(f"[OK] GIF created: {os.path.basename(result)} ({size_kb:.1f} KB)")
                return True
            else:
                print(f"[FAIL] GIF not created as expected: {result}")
                return False
    except Exception as e:
        print(f"[FAIL] GIF creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_video_creation():
    """Test MP4 creation with MoviePy."""
    print("\n=== Testing MP4 Creation (MoviePy) ===")
    
    try:
        from moviepy.editor import ImageClip, concatenate_videoclips
        print("[OK] MoviePy import successful")
    except ImportError as e:
        print(f"[SKIP] MoviePy not available: {e}")
        return None
    
    try:
        from image_generator import create_images
        from video_editor import create_video
        
        with tempfile.TemporaryDirectory() as tmpdir:
            images = create_images("Video test", num_images=3, output_folder=tmpdir)
            output_path = os.path.join(tmpdir, "test.mp4")
            
            print("[INFO] Creating video (may take 30-60 seconds)...")
            result = create_video(images, "", output_path)
            
            if result.endswith('.mp4') and os.path.exists(result):
                size_kb = os.path.getsize(result) / 1024
                print(f"[OK] MP4 created: {os.path.basename(result)} ({size_kb:.1f} KB)")
                return True
            else:
                print(f"[FAIL] MP4 not created as expected: {result}")
                return False
    except Exception as e:
        print(f"[FAIL] MP4 creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("VIDEO GENERATION PIPELINE TEST")
    print("=" * 60)
    
    results = {}
    
    results['dependencies'] = test_dependencies()
    results['images'] = test_image_creation()
    results['gif'] = test_gif_creation()
    results['video'] = test_video_creation()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "PASS" if result is True else ("SKIP" if result is None else "FAIL")
        print(f"[{status}] {test_name.replace('_', ' ').title()}")
    
    all_passed = all(v is not False for v in results.values())
    
    if all_passed:
        print("\n[SUCCESS] All tests passed! Ready for deployment.")
        return 0
    else:
        print("\n[WARNING] Some tests failed. Check output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
