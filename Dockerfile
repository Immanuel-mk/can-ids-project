FROM python:3.11-slim

WORKDIR /app

# System dependencies (SocketCAN tools)
RUN apt-get update && apt-get install -y \
    iproute2 \
    can-utils \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make scripts executable
RUN chmod +x setup_vcan.sh run.sh

# Default command
CMD ["bash", "run.sh"]
