# Custom n8n image for Hugging Face Spaces
FROM n8nio/n8n:latest

USER root

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    ffmpeg \
    curl \
    git

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

# Hugging Face Space specific setup
# HF uses port 7860 by default
ENV N8N_PORT=7860
EXPOSE 7860

# Ensure the .n8n directory is writable by the node user
RUN mkdir -p /home/node/.n8n && chown -R node:node /home/node/.n8n
RUN mkdir -p /home/node/scripts && chown -R node:node /home/node/scripts
RUN mkdir -p /home/node/output && chown -R node:node /home/node/output

USER node

# Set environment variables for DB persistence (to be provided via HF Secrets)
# These will tell n8n to use Supabase as its database
ENV DB_TYPE=postgresdb

WORKDIR /home/node
