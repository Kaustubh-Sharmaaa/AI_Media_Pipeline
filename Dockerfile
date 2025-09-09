FROM python:3.9-slim

# System dependencies for OCR, TTS, and build tools
RUN echo "=== Installing system dependencies ===" && \
    apt-get update && \
    apt-get install -y tesseract-ocr espeak espeak-ng espeak-ng-data ffmpeg build-essential git && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy all code from the build context (project root)
RUN echo "=== Copying project files ==="
COPY . /app

# Install Python dependencies (combine all requirements)
RUN echo "=== Installing Python dependencies: orchestrator ===" && \
    pip install --upgrade pip && \
    pip install -r ai_media_pipeline/orchestrator/requirements.txt

RUN echo "=== Installing Python dependencies: transcribe ===" && \
    pip install -r ai_media_pipeline/transcribe/requirements.txt

RUN echo "=== Installing Python dependencies: interpret ===" && \
    pip install -r ai_media_pipeline/interpret/requirements.txt && \
    python3 -m spacy download en_core_web_sm

RUN echo "=== Installing Python dependencies: extract ===" && \
    pip install -r ai_media_pipeline/extract/requirements.txt

RUN echo "=== Installing Python dependencies: synthesize ===" && \
    pip install -r ai_media_pipeline/synthesize/requirements.txt

# Expose a volume for outputs (optional)
VOLUME ["/app/ai_media_pipeline/outputs"]

# Default entrypoint: CLI orchestrator
ENTRYPOINT ["python3", "-m", "ai_media_pipeline.orchestrator.app"] 
