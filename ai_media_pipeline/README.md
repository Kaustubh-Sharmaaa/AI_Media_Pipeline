# AI Media & Data Processing Pipeline

This package contains a modular, containerized pipeline for:
- Speech-to-text (audio -> text)
- Intent extraction (text -> structured params)
- Text-to-speech (text -> audio)
- OCR (image -> text)
- Unified orchestration via a Typer CLI and optional FastAPI server

## How to Use

### A. Native Python (Local)
```sh
# Example: Transcribe audio
PYTHONPATH=. python3 ai_media_pipeline/orchestrator/app.py --file ai_media_pipeline/samples/input.wav --output ai_media_pipeline/outputs/input.json

# Example: OCR document
PYTHONPATH=. python3 ai_media_pipeline/orchestrator/app.py --file ai_media_pipeline/samples/registration_document.png --output ai_media_pipeline/outputs/registration.json

# Example: Text-to-speech and intent extraction
PYTHONPATH=. python3 ai_media_pipeline/orchestrator/app.py --file ai_media_pipeline/samples/sample.txt --output ai_media_pipeline/outputs/sample_reply.wav
```

### B. Docker
```sh
docker build -t ai-media-pipeline .

docker run --rm \
  -v $(pwd)/ai_media_pipeline/samples:/app/ai_media_pipeline/samples \
  -v $(pwd)/ai_media_pipeline/outputs:/app/ai_media_pipeline/outputs \
  ai-media-pipeline \
  --file ai_media_pipeline/samples/input.wav \
  --output ai_media_pipeline/outputs/input.json
```

### C. Docker Compose
```sh
docker-compose up --build
```
- To override, run: `docker-compose run orchestrator --file ai_media_pipeline/samples/sample.txt --output ai_media_pipeline/outputs/sample_reply.wav`

## Notes
- Python imports and module paths use `ai_media_pipeline.*`.
- Samples directory is at `ai_media_pipeline/samples` and outputs at `ai_media_pipeline/outputs`.
