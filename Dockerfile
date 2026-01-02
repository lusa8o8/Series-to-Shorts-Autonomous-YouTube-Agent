# Custom n8n image with Python, FFmpeg, and yt-dlp
FROM n8nio/n8n:latest

USER root

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    ffmpeg \
    curl

# Create virtual environment and install Python libraries
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install \
    yt-dlp \
    supabase \
    huggingface_hub \
    psutil \
    pandas

USER node
