#!/usr/bin/env bash
# Automatic1111 per-shot txt2img commands
# Usage: edit MODEL_PATH and other flags as needed, then run this script in your Automatic1111 environment.

OUTDIR="outputs/striker_short"
mkdir -p "$OUTDIR"

# Replace or export MODEL_PATH if your environment needs it; Automatic1111's txt2img.py uses the current WebUI environment.

# Shot 1 - Wide tracking
python scripts/txt2img.py \
  --prompt "Cinematic broadcast-style football match, photorealistic. A striker in a red-and-white jersey sprints down the right flank. Wide composition, emphasize field breadth and crowd, low-angle tracking camera, motion blur" \
  --negative_prompt "lowres, watermark, text, logo, jersey-branding" \
  --sampler "DPM++" --cfg_scale 8 --steps 30 --width 1920 --height 1080 --n_samples 1 --seed 12345 --outdir "$OUTDIR/shot01"

# Shot 2 - Medium close tracking
python scripts/txt2img.py \
  --prompt "Cinematic broadcast-style football match, medium close, low-angle, rim lighting on jersey, motion blur on ball" \
  --negative_prompt "lowres, watermark, text, logo, jersey-branding" \
  --sampler "DPM++" --cfg_scale 9 --steps 36 --width 1920 --height 1080 --n_samples 1 --seed 23456 --outdir "$OUTDIR/shot02"

# Shot 3 - Over-the-shoulder cut inside
python scripts/txt2img.py \
  --prompt "Over-the-shoulder toward goal, player cutting inside, curved ball trajectory emphasized" \
  --negative_prompt "lowres, watermark, text, logo, jersey-branding" \
  --sampler "DPM++" --cfg_scale 9 --steps 36 --width 1920 --height 1080 --n_samples 1 --seed 34567 --outdir "$OUTDIR/shot03"

# Shot 4 - Close-up on strike
python scripts/txt2img.py \
  --prompt "Extreme close-up on boot striking ball with micro-details, high shutter clarity on contact, micro dust/spark" \
  --negative_prompt "lowres, watermark, text, logo, jersey-branding" \
  --sampler "DPM++" --cfg_scale 10 --steps 40 --width 1280 --height 720 --n_samples 1 --seed 45678 --outdir "$OUTDIR/shot04"

# Shot 5 - Follow-through long shot
python scripts/txt2img.py \
  --prompt "Long follow shot, ball curve emphasized, top-corner trajectory, crowd bokeh, smooth tracking" \
  --negative_prompt "lowres, watermark, text, logo, jersey-branding" \
  --sampler "DPM++" --cfg_scale 9 --steps 36 --width 1920 --height 1080 --n_samples 1 --seed 56789 --outdir "$OUTDIR/shot05"

# Shot 6 - Goal frame and freeze
python scripts/txt2img.py \
  --prompt "Goal-frame, high drama, freeze or slow-motion, scoreboard overlay optional, cinematic grade" \
  --negative_prompt "lowres, watermark, text, logo, jersey-branding" \
  --sampler "DPM++" --cfg_scale 8.5 --steps 30 --width 1920 --height 1080 --n_samples 1 --seed 67890 --outdir "$OUTDIR/shot06"

echo "Automatic1111 per-shot commands created. Edit seeds and prompts as desired."
