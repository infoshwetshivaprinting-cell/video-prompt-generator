# Video Generation Debug Guide

## Changes Made to Fix Silent Failures

### 1. Enhanced `video_editor.py`
- **Added detailed stderr logging** for all critical operations
- **Explicit error reporting** for moviepy import failures
- **Per-operation logging** with `[VIDEO_EDITOR]` prefix for easy filtering
- **Improved encoding settings** for Streamlit Cloud (faster preset, limited threads)
- **Better fallback mechanism** that logs when switching to GIF

### 2. Enhanced `streamlit_app.py`
- **Expanded error UI** to show full exception tracebacks in expander
- **Better error capture** using `traceback.format_exc()`
- **Debug information** now includes detailed error context

### 3. Updated `requirements.txt`
- Added `numpy` and `decorator` (required by moviepy)
- Changed imageio pinning to allow newer versions
- Improved dependency resolution for Streamlit Cloud

---

## Troubleshooting Steps

### Step 1: Check Streamlit Cloud Logs
After clicking "Generate Short", check your Streamlit Cloud logs for messages starting with `[VIDEO_EDITOR]`:

```
[VIDEO_EDITOR] MoviePy import failed: ...
[VIDEO_EDITOR] Creating video with N clips...
[VIDEO_EDITOR] Falling back to GIF creation...
```

### Step 2: Identify the Failure Point

| Log Message | Meaning | Solution |
|---|---|---|
| `MoviePy import failed: No module named 'moviepy'` | moviepy not installed | Reinstall requirements.txt on Streamlit Cloud |
| `No valid images found` | Image paths are invalid | Check image_generator.py output |
| `FFmpeg not found` | ffmpeg codecs missing | GIF fallback should work |
| `Falling back to GIF creation` | Normal behavior if moviepy fails | GIF creation should succeed |

### Step 3: Check GIF Creation

If you see "Falling back to GIF creation", the GIF should be generated without audio. Check:
- Error message in the "Video Error Details" expander
- Output folder for `.gif` files (check using Debug Information expander)

### Step 4: Local Testing

Run this Python snippet locally to test each component:

```python
from video_editor import create_video
from image_generator import create_images

# Create test images
images = create_images("Test prompt", num_images=3, output_folder="test_output")
print(f"Created {len(images)} images")

# Try to create video
video_path = create_video(images, "", "test_output/test.mp4")
print(f"Video created at: {video_path}")
```

---

## Performance Optimization Applied

- **Encoding preset**: Changed from `'medium'` to `'fast'` for Streamlit Cloud
- **Thread limit**: Set `threads=2` to respect Streamlit Cloud resource limits
- **Fallback**: GIF creation uses pure Python (no ffmpeg needed)
- **Async logging**: All logging goes to stderr (non-blocking)

---

## Expected Behavior After Fix

### Success Path:
1. ? Voiceover generated
2. ? Images created
3. ? Video created (MP4) OR GIF created
4. ? Download available

### Fallback Path (if moviepy fails):
1. ? Voiceover generated
2. ? Images created
3. ? Fallback to GIF
4. ? GIF download available (no audio)

---

## Monitoring in Streamlit Cloud

Visit https://video-prompt-generator-d6ij3vavjrhhq5jkaoke2b.streamlit.app and:

1. Open browser DevTools (F12)
2. Go to **Network** tab
3. Generate a short
4. Check console logs for `[VIDEO_EDITOR]` messages
5. Review the "Debug Information" and "Video Error Details" expanders

---

## If Issues Persist

1. Check `requirements.txt` is deployed correctly
2. Verify ffmpeg availability: `which ffmpeg` (in Streamlit Cloud shell)
3. Test moviepy locally: `python -c "from moviepy.editor import *; print('OK')"`
4. Check file permissions in `/tmp` directory
5. Review Streamlit Cloud resource limits (memory/CPU)
