# Receptro.AI Modular Media & Data Processing Pipeline

This project provides a modular, containerized pipeline for:
- **Speech-to-text transcription** (audio → text)
- **Intent extraction** (text → structured intent/parameters)
- **Text-to-speech synthesis** (text → audio)
- **OCR and structured data extraction** (image → structured text)
- **Unified orchestration via CLI (and Docker/Compose)**

---

## **Capabilities**

### **1. Audio File Processing**
- Supported: `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`
- Pipeline: Transcribes audio → extracts intent/parameters → outputs JSON

### **2. Image File Processing (OCR)**
- Supported: `.png`, `.jpg`, `.jpeg`
- Pipeline: Extracts all text from image using Tesseract OCR → outputs JSON

### **3. Text File Processing (Intent + TTS)**
- Supported: `.txt`
- Pipeline: Extracts intent/parameters from text → synthesizes reply as WAV

### **4. Orchestration**
- Unified CLI interface (Typer-based)
- Docker and Docker Compose support for reproducible, portable runs

---

## **How to Use**

### **A. Native Python (Local)**
```sh
# Example: Transcribe audio
PYTHONPATH=. python3 receptro_ai_pipeline/orchestrator/app.py --file receptro_ai_pipeline/samples/input.wav --output receptro_ai_pipeline/outputs/input.json

# Example: OCR document
PYTHONPATH=. python3 receptro_ai_pipeline/orchestrator/app.py --file receptro_ai_pipeline/samples/registration_document.png --output receptro_ai_pipeline/outputs/registration.json

# Example: Text-to-speech and intent extraction
PYTHONPATH=. python3 receptro_ai_pipeline/orchestrator/app.py --file receptro_ai_pipeline/samples/sample.txt --output receptro_ai_pipeline/outputs/sample_reply.wav
```

### **B. Docker**

**Build the image:**
```sh
docker build -t receptro-ai-pipeline ./receptro_ai_pipeline/orchestrator/
```

**Run the CLI:**
```sh
docker run --rm \
  -v $(pwd)/receptro_ai_pipeline/samples:/app/receptro_ai_pipeline/samples \
  -v $(pwd)/receptro_ai_pipeline/outputs:/app/receptro_ai_pipeline/outputs \
  receptro-ai-pipeline \
  --file receptro_ai_pipeline/samples/input.wav \
  --output receptro_ai_pipeline/outputs/input.json
```

### **C. Docker Compose**

**From `receptro_ai_pipeline/orchestrator/`:**
```sh
docker-compose up --build
```
- To override the command, edit `docker-compose.yml` or use:
  ```sh
  docker-compose run orchestrator --file receptro_ai_pipeline/samples/sample.txt --output receptro_ai_pipeline/outputs/sample_reply.wav
  ```

---

## **Extensibility & Swapping Engines**
- Swap transcription, NLU, TTS, or OCR engines by updating the relevant module and requirements.

---

## **Project Structure**
- Each module (`transcribe`, `interpret`, `synthesize`, `extract`) is self-contained with its own requirements and tests.
- All orchestration and Docker/Compose files are in `orchestrator/`.

---

## **Project Requirements Coverage**

| Requirement                                 | Status      |
|----------------------------------------------|-------------|
| Project structure & modularization           | ✅ Complete |
| Speech-to-text (Whisper)                     | ✅ Complete |
| Intent extraction (spaCy)                    | ✅ Complete |
| Text-to-speech (pyttsx3, local)              | ✅ Complete |
| OCR (Tesseract)                              | ✅ Complete |
| CLI orchestrator (Typer)                     | ✅ Complete |
| Dockerfile                                   | ✅ Complete |
| Docker Compose                               | ✅ Complete |
| Sample input/output files                    | ✅ Complete |
| README with usage and rationale              | ✅ Complete |
| Config file (`config.yaml`)                  | ⬜ Minimal, can be expanded |
| Unit tests for each module                   | ⬜ Stubs exist, but not all modules have full tests |
| HTTP interface (FastAPI)                     | ⬜ Not implemented (optional) |
| Template-based/ML-based field extraction     | ⬜ Only raw OCR, no field mapping yet |
| Task tracking (`TASKS.md`)                   | ⬜ Needs updating as tasks progress |

---

## **What’s Missing or Could Be Improved**
- **Field mapping in OCR:** Only raw text is extracted; no structured field extraction (e.g., extracting name, VIN, etc. as fields).
- **Unit tests:** Some modules lack full test coverage.
- **Config management:** `config.yaml` is present but not actively used.
- **HTTP API:** Not implemented (optional per instructions).
- **Task tracking:** `TASKS.md` should be updated as you progress.
