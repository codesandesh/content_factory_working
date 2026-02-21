FROM n8nio/n8n:1.76.0

USER root

# Install FFmpeg and Python
RUN apk add --no-cache ffmpeg python3 py3-pip

# Install yt-dlp
RUN pip3 install yt-dlp --break-system-packages

USER node
