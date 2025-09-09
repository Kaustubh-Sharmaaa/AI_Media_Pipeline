# AI Media & Data Processing Pipeline

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
docker build -t ai-media-pipeline ./receptro_ai_pipeline/orchestrator/
```

**Run the CLI:**
```sh
docker run --rm \
  -v $(pwd)/receptro_ai_pipeline/samples:/app/receptro_ai_pipeline/samples \
  -v $(pwd)/receptro_ai_pipeline/outputs:/app/receptro_ai_pipeline/outputs \
  ai-media-pipeline \
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

## **Feature Overview**
- Speech-to-text (Whisper)
- Intent extraction (spaCy)
- Text-to-speech (pyttsx3, local)
- OCR (Tesseract)
- CLI orchestrator (Typer)
- Docker and Docker Compose

## **What’s Missing or Could Be Improved**
- **Field mapping in OCR:** Only raw text is extracted; no structured field extraction (e.g., extracting name, VIN, etc. as fields).
- **Unit tests:** Some modules lack full test coverage.
- **Config management:** `config.yaml` is present but not actively used.
- **HTTP API:** Not implemented (optional per instructions).
- **Task tracking:** `TASKS.md` should be updated as you progress.

---

## Development Notes

### Project Motivation
This project is a modular, production-grade pipeline for media and data processing, suitable for real-world applications and as a showcase for advanced Python, ML, and DevOps skills. The goals include:
- Transcribe speech from audio files
- Extract intent and parameters from text
- Convert text replies back into audio
- Extract structured data from photographed documents
- Orchestrate all steps via CLI or HTTP API
- Be easily containerized and reproducible
- Provide a user-friendly web UI for demonstration

### Key Design Decisions
- **Modular Architecture:** Each major function (transcribe, interpret, synthesize, extract) is a separate module with its own dependencies and tests.
- **CLI-first, then API:** Started with a Typer CLI for orchestration, then added a FastAPI HTTP API and web UI for broader usability.
- **Open Source Engines:** Used OpenAI Whisper (STT), spaCy (NLU), pyttsx3 (TTS), and pytesseract (OCR) to avoid paid APIs and ensure local/offline capability.
- **Containerization:** Docker and Docker Compose for reproducibility and easy deployment.
- **Comprehensive Documentation:** All steps, challenges, and solutions are documented for transparency and as a CV artifact.

### Development & Debugging Highlights
- **Path and Import Issues:** Resolved Python import errors by standardizing on `receptro_ai_pipeline` and using `PYTHONPATH=.`.
- **Missing Sample Files:** Created and documented sample input files for all pipeline stages.
- **Module Implementation:** Implemented missing functions (`parse_document`, `text_to_speech`) as needed, with robust error handling.
- **Docker Build Fixes:** Addressed missing system dependencies (e.g., `git`, `build-essential`), Whisper install from GitHub, and spaCy model download in Docker.
- **API & UI Iteration:** Refined the FastAPI endpoints and web UI, fixing issues with route registration, file handling, and JavaScript error handling.
- **Logging:** Added detailed logging to both backend and frontend for easier debugging and transparency.
- **User Feedback Loop:** Iteratively improved the UI and API based on real user feedback and error reports.

### What This Project Demonstrates
- Full-stack Python skills from ML/NLP to web APIs and frontend JS
- Production-readiness: modular, testable, containerized, and documented
- Real-world relevance: media and document processing across industries
- Problem-solving: ability to debug, refactor, and deliver under constraints

---

## HTTP API & Web UI Documentation

### FastAPI Endpoints

#### `POST /process`
- **Description:** Unified endpoint for all pipeline steps (audio, image, or text input).
- **Consumes:** `multipart/form-data`
- **Parameters:**
  - `file`: (required) Audio, image, or text file
  - `voice`: (optional, for TTS)
  - `rate`: (optional, for TTS)
- **Returns:**
  - For audio/image: JSON with transcription/intent or OCR result
  - For text: WAV audio file (TTS reply)

##### Example: Audio File (Speech-to-Text + Intent)
Request:
```bash
curl -F "file=@samples/input.wav" http://localhost:8000/process
```
Response (JSON):
```json
{
  "transcription": {
    "text": "Hi, I would like to get information about the car that I checked out yesterday. The Ford Mustang GT which was in red.",
    "confidence": 0.47,
    "timestamps": [ ... ]
  },
  "intent": {
    "intent": "get_information",
    "params": {
      "car_make": "Ford",
      "car_model": "Mustang GT",
      "color": "red",
      "date": "yesterday"
    }
  }
}
```

##### Example: Image File (OCR)
Request:
```bash
curl -F "file=@samples/registration_document.png" http://localhost:8000/process
```
Response (JSON):
```json
{
  "text": "STATE VEHICLE REGISTRATION\nCERTIFICATE\nRegistration No.: ..."
}
```

##### Example: Text File (TTS)
Request:
```bash
curl -F "file=@samples/sample.txt" http://localhost:8000/process
```
Response: WAV audio file (Content-Type: audio/wav)

---

### Web UI
- **Access:** [http://localhost:8000/](http://localhost:8000/)
- **Features:**
  1. Upload audio file → see transcription and intent
  2. Upload image file → see OCR result
  3. Edit/generate reply text → download TTS audio
- **Sequential workflow:** Each step enables the next, with auto-generated summary replies.
- **Robust error handling:** All errors and raw responses are logged in the browser console for debugging.

---

## API/Module Dependencies

- **Orchestrator:** typer, fastapi, uvicorn, pyyaml, pydantic
- **Transcribe:** openai-whisper, pydub
- **Interpret:** spacy
- **Synthesize:** pyttsx3
- **Extract:** pytesseract, opencv-python

---

## Example Inputs & Outputs

### Sample Inputs
- `samples/input.wav` — Example audio query
- `samples/registration_document.png` — Example car registration document
- `samples/sample.txt` — Example text query

### Sample Outputs
- `outputs/input.json` — Transcription + intent extraction result
- `outputs/registration.json` — OCR result
- `outputs/sample_reply.wav` — TTS reply audio

---

## Configuration
- `orchestrator/config.yaml` is present for future engine/module settings (currently minimal).

---

## Testing
- Each module includes unit/integration tests (coverage varies).

---

## Troubleshooting & Tips
- If you see import errors, ensure you run with `PYTHONPATH=.` from the project root.
- For Docker, ensure all sample and output directories are mounted as volumes.
- For Whisper, spaCy, and Tesseract, ensure all dependencies are installed (see requirements.txt in each module).
- Use browser console and backend logs for debugging API/UI issues.

---

## Limitations: TTS Voice Quality in Docker
- The current TTS engine (pyttsx3 with espeak-ng) is fully offline and open source, but the generated voice quality in Docker containers is basic/robotic compared to desktop systems.
- This is a known limitation of espeak-ng and open-source TTS in headless/server environments.
- For production or demo use where high-quality voices are required, consider integrating a neural TTS engine (e.g., Coqui TTS) or a cloud-based service (note: may require internet and/or paid API).
- All other pipeline steps (STT, OCR, NLU) work fully offline and as expected in Docker.

---
