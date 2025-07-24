# Chat Render to MP4

**Chat Render to MP4** is a Python tool that reads chat logs from a JSON file and renders them into a video using Pillow and FFmpeg.

---

## Features

- Renders chat messages with usernames and timestamps
- Parses from static JSON chat logs
- Saves each chat state as an image frame
- Simple to customize and extend

**No emote or emoji rendering at this time**

---

## Requirements

- Python 3.x
- [Pillow](https://pypi.org/project/Pillow/)
- [FFmpeg](https://ffmpeg.org/) (Included with files)

Install Python dependencies:

```bash
pip install Pillow
