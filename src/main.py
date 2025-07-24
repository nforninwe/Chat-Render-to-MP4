from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
import json

# Constants
WIDTH, HEIGHT = 400, 600
BACKGROUND_COLOR = (24, 24, 24)
USER_COLOR = (0, 150, 255)
MESSAGE_COLOR = (255, 255, 255)
TIMESTAMP_COLOR = (150, 150, 150)
FONT_SIZE = 20
LINE_HEIGHT = 35
MARGIN = 10
OUTPUT_DIR = "frames"
VIDEO_OUTPUT = "chat_video.mp4"
CHAT_FILE = "chat_data.json"

# Load chat data from file
with open(CHAT_FILE, 'r', encoding='utf-8') as f:
    chat_data = json.load(f)

# Load a font
try:
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
except IOError:
    font = ImageFont.load_default()

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to draw a single message
def draw_message(draw, username, message, timestamp, position):
    user_text = f"{username}: "
    ts_text = f"[{timestamp[11:16]}]"  # Format: HH:MM
    user_text_width = draw.textlength(user_text, font=font)
    draw.text((MARGIN, position), ts_text, font=font, fill=TIMESTAMP_COLOR)
    draw.text((MARGIN + 70, position), user_text, font=font, fill=USER_COLOR)
    draw.text((MARGIN + 70 + user_text_width, position), message, font=font, fill=MESSAGE_COLOR)

# Frame rendering loop
rendered_messages = []
for i, chat in enumerate(chat_data["chat"]):
    rendered_messages.append((chat["sender"], chat["message"], chat["timestamp"]))

    # Create blank image
    image = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    # Draw all messages so far
    y = MARGIN
    for sender, msg, ts in rendered_messages:
        draw_message(draw, sender, msg, ts, y)
        y += LINE_HEIGHT
        if y > HEIGHT - MARGIN:
            break  # stop drawing when out of space

    # Save frame to disk
    filename = os.path.join(OUTPUT_DIR, f"frame_{i:03d}.png")
    image.save(filename)
    print(f"Saved {filename}")

# Run FFmpeg to create the video
print("Rendering video with FFmpeg...")
ffmpeg_cmd = [
    "ffmpeg",
    "-y",
    "-framerate", "1",
    "-i", os.path.join(OUTPUT_DIR, "frame_%03d.png"),
    "-c:v", "libx264",
    "-r", "30",
    "-pix_fmt", "yuv420p",
    VIDEO_OUTPUT
]

try:
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"Video rendered to {VIDEO_OUTPUT}")
except subprocess.CalledProcessError as e:
    print("FFmpeg failed:", e)
