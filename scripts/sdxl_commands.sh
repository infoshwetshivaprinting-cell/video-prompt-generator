#!/usr/bin/env bash
# SDXL per-shot CLI commands (example). Replace sdxl_cli with your model runner's CLI.
# Adjust MODEL, OUTPUT_DIR, SEED, and CLI flags as needed for your environment.

MODEL="/path/to/sdxl_model"
OUTPUT_DIR="output/frames"
mkdir -p "$OUTPUT_DIR"

# Shot 1 - Wide tracking
sdxl_cli --model "$MODEL" \
  --prompt "Cinematic broadcast-style football match, photorealistic. A striker in a red-and-white jersey sprints down the right flank. Wide composition, emphasize field breadth and crowd, low-angle tracking camera, motion blur" \
  --width 1920 --height 1080 --cfg 8.0 --sampler dpmpp --steps 30 --seed 12345 \
  --out "$OUTPUT_DIR/shot01_wide_12345.png"

# Shot 2 - Medium close tracking
sdxl_cli --model "$MODEL" \
  --prompt "Medium close, low-angle, rim lighting on jersey, motion blur on ball, waist-height tracking" \
  --width 1920 --height 1080 --cfg 9.0 --sampler dpmpp --steps 36 --seed 23456 \
  --out "$OUTPUT_DIR/shot02_medium_23456.png"

# Shot 3 - Over-the-shoulder cut inside
sdxl_cli --model "$MODEL" \
  --prompt "Over-the-shoulder toward goal, player cutting inside, curved ball trajectory emphasized, cinematic lighting" \
  --width 1920 --height 1080 --cfg 9.0 --sampler dpmpp --steps 36 --seed 34567 \
  --out "$OUTPUT_DIR/shot03_ots_34567.png"

# Shot 4 - Close-up on strike
sdxl_cli --model "$MODEL" \
  --prompt "Extreme close-up on boot striking ball with micro-details, high shutter clarity on contact, micro dust/spark" \
  --width 1280 --height 720 --cfg 10.0 --sampler dpmpp --steps 40 --seed 45678 \
  --out "$OUTPUT_DIR/shot04_close_45678.png"

# Shot 5 - Follow-through long shot
sdxl_cli --model "$MODEL" \
  --prompt "Long follow shot, ball curve emphasized, top-corner trajectory, crowd bokeh, smooth tracking" \
  --width 1920 --height 1080 --cfg 9.0 --sampler dpmpp --steps 36 --seed 56789 \
  --out "$OUTPUT_DIR/shot05_follow_56789.png"

# Shot 6 - Goal frame and freeze
sdxl_cli --model "$MODEL" \
  --prompt "Goal-frame, high drama, freeze or slow-motion, scoreboard overlay optional, cinematic grade" \
  --width 1920 --height 1080 --cfg 8.5 --sampler dpmpp --steps 30 --seed 67890 \
  --out "$OUTPUT_DIR/shot06_goal_67890.png"

echo "SDXL per-shot commands completed (replace sdxl_cli with your runner and adjust MODEL path)."
