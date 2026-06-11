# Requirements & Dependencies Documentation

## Overview

This project uses Python 3.11.6 with carefully managed dependencies for video generation and Streamlit cloud deployment.

---

## Installation

### Production Setup (Streamlit Cloud)
```bash
pip install -r requirements.txt
```

This installs all necessary packages for running the video prompt generator application.

### Development Setup (Local)
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development tools and optional features
pip install -r dev-requirements.txt
```

---

## Requirements Files

### `requirements.txt` (Production)

**Core Dependencies:**
- `streamlit==1.29.0` - Web UI framework
- `moviepy==1.0.3` - Video creation library
- `Pillow>=9.5.0,<10.0.0` - Image processing (fallback for video)
- `gTTS==2.3.2` - Google Text-to-Speech

**Utilities:**
- `python-dotenv==1.0.0` - Environment variable management
- `requests==2.31.0` - HTTP client (used by ElevenLabs TTS)
- `pytest==7.4.0` - Testing framework

**Media Processing:**
- `imageio>=2.31.1` - Image I/O library
- `imageio-ffmpeg>=0.4.8` - FFmpeg backend for imageio

**MoviePy Dependencies (Auto-installed):**
- `numpy>=1.24.0` - Required by moviepy for array operations
- `decorator>=5.1.0` - Required by moviepy for decorators

**Build Tools:**
- `setuptools>=65.5.0` - Package building
- `wheel` - Wheel distribution format

### `dev-requirements.txt` (Development Only)

**Testing:**
- `pytest>=7.4.0` - Unit testing
- `pytest-cov>=4.1.0` - Code coverage reports
- `black>=23.0.0` - Code formatting

**Code Quality:**
- `flake8>=6.0.0` - Linting

**Optional TTS Providers:**
- `pyttsx3>=2.90` - Offline text-to-speech (for testing)
- `google-cloud-texttospeech` - Google Cloud TTS (if needed)

**Development Tools:**
- `streamlit-extras>=0.3.0` - Additional Streamlit components

### `runtime.txt` (Streamlit Cloud)

```
python-3.11.6
```

Specifies the Python version for Streamlit Cloud deployment.

---

## Dependency Analysis

### Core Dependencies

| Package | Version | Purpose | Notes |
|---------|---------|---------|-------|
| streamlit | 1.29.0 | Web UI | Latest stable for Python 3.11 |
| moviepy | 1.0.3 | Video generation | Core feature |
| Pillow | 9.5.0+ | Image processing | GIF fallback if moviepy fails |
| gTTS | 2.3.2 | Text-to-speech | Default TTS provider |
| imageio | 2.31.1+ | Media I/O | For moviepy |
| imageio-ffmpeg | 0.4.8+ | FFmpeg wrapper | Video encoding |

### Optional TTS Providers

| Provider | Package | Status | Notes |
|----------|---------|--------|-------|
| gTTS (Google) | gTTS | ? Included | Free, requires internet |
| pyttsx3 | pyttsx3 | ?? Optional | Offline, local voices |
| ElevenLabs | requests | ? Included | Premium, API key required |
| Google Cloud | google-cloud-texttospeech | ?? Optional | Enterprise, auth required |

---

## Version Compatibility

### Python Version
- **Recommended:** Python 3.11.6
- **Tested:** Python 3.11.x
- **Minimum:** Python 3.9 (estimated)

### Streamlit Cloud
- Uses `runtime.txt` to specify Python 3.11.6
- Auto-installs from `requirements.txt`

### Known Compatibility

| Package | Min Version | Current | Max Version |
|---------|------------|---------|-------------|
| streamlit | 1.0.0 | 1.29.0 | Latest |
| moviepy | 1.0.0 | 1.0.3 | 1.1.0 |
| Pillow | 9.5.0 | 9.5.0+ | <10.0.0 |
| numpy | 1.24.0 | 1.24.0+ | Latest |
| decorator | 5.1.0 | 5.1.0+ | Latest |

---

## Installation Verification

### Test Production Setup
```bash
pip install -r requirements.txt
python run_app_check.py
```

Expected output:
```
Imported config
Imported voiceover_generator
Imported image_generator
Imported video_editor
Imported seo_helper
Imported logger
All basic modules import successfully.
```

### Test Video Generation
```bash
pip install -r requirements.txt
python test_video_pipeline.py
```

Expected results:
- [OK] Dependencies
- [OK] Images
- [OK] GIF (or SKIP if moviepy unavailable)
- [OK] Video (or SKIP if moviepy unavailable)

---

## Deployment Procedures

### Local Testing
```bash
# Install all dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

### Streamlit Cloud Deployment
1. Push to GitHub: `git push origin main`
2. Streamlit Cloud reads `requirements.txt` and `runtime.txt`
3. Automatically installs dependencies
4. Deploys application

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11.6-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "streamlit_app.py"]
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named X"

**Solution:**
```bash
# Reinstall all requirements
pip install -r requirements.txt --force-reinstall

# Verify installation
python run_app_check.py
```

### "moviepy not found - using GIF fallback"

**Expected behavior** if:
- ffmpeg not installed on system
- Or moviepy dependencies missing
- GIF generation should still work with Pillow

**To fix:**
```bash
pip install moviepy>=1.0.3
# Or install ffmpeg system package (varies by OS)
```

### "gTTS network error"

**Possible causes:**
- No internet connection
- Google API rate limit exceeded
- Network firewall blocking

**Solution:**
- Try again later
- Or use offline provider: `pyttsx3`
- Or use premium provider with credentials

### Import errors on Streamlit Cloud

**Common cause:** Dependencies not listed in requirements.txt

**Solution:**
```bash
# Add missing package
echo "missing-package>=1.0.0" >> requirements.txt
git add requirements.txt
git commit -m "Add missing dependency"
git push origin main
```

---

## Maintenance

### Keeping Dependencies Updated

**Monthly:**
```bash
pip list --outdated
```

**Update strategy:**
- Security updates: ASAP
- Bug fix updates: Next sprint
- Feature updates: Evaluate for breaking changes

### Adding New Dependencies

**For production use:**
```bash
# Test locally
pip install new-package

# Verify in code
# Test extensively

# Add to requirements.txt with specific version
echo "new-package==X.Y.Z" >> requirements.txt

# Commit and deploy
git add requirements.txt
git commit -m "Add new-package for feature X"
git push origin main
```

**For development only:**
```bash
# Add to dev-requirements.txt
echo "dev-package>=X.Y.Z" >> dev-requirements.txt
```

---

## Performance & Resource Optimization

### Memory Usage
- Streamlit Cloud: ~512 MB RAM allocated
- Video generation: ~500-800 MB peak during encoding
- GIF generation: ~200-300 MB peak

### CPU Usage
- Video encoding: Multi-threaded (limited to 2 threads)
- Image processing: Single-threaded
- TTS generation: Depends on provider

### Recommendations
- Limit to 10 images per generation
- Use GIF fallback on limited systems
- Monitor Streamlit Cloud resource metrics

---

## Security Notes

### Dependencies
- All packages vetted for common security issues
- Using stable versions with known histories
- No known CVEs in current versions

### API Keys
- Store in Streamlit secrets (Streamlit Cloud)
- Or use .env file locally
- Never commit API keys to repository

### Environment Variables
```bash
# Local development
ELEVENLABS_API_KEY=xxx
ELEVENLABS_VOICE_ID=yyy

# Streamlit Cloud
# Set via dashboard secrets manager
```

---

## License Compliance

All dependencies use compatible open-source licenses:
- streamlit: Apache 2.0
- moviepy: MIT
- Pillow: HPND
- gTTS: MIT
- requests: Apache 2.0

---

## Support & Resources

### Documentation
- Streamlit: https://docs.streamlit.io/
- MoviePy: https://zulko.github.io/moviepy/
- Pillow: https://pillow.readthedocs.io/

### Issue Resolution
1. Check COMPLETE_AUDIT.md for dependency analysis
2. Run test_video_pipeline.py for diagnostics
3. Check Streamlit Cloud logs
4. Review VIDEO_DEBUG_GUIDE.md for troubleshooting

---

**Last Updated:** 2026-06-11
**Status:** ? Complete and Validated
