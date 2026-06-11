import logging
import os

# Configure logging settings
LOG_FILE = os.path.join("logs", "video_generator.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

# Example usage
if __name__ == "__main__":
    log_info("Video generation started.")
    try:
        # Simulate process
        print("Processing...")
    except Exception as e:
        log_error(f"Error: {e}")
    finally:
        log_info("Video generation ended.")