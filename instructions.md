**Cursor AI Agent Instructions for Receptro.AI Modular Media & Data Processing Pipeline**

This document provides a comprehensive, step-by-step guide for AI agents (e.g., Cursor) to design, implement, and deliver an end-to-end solution that:

1. Transcribes speech from audio files into text
2. Infers intent and parameters from text
3. Synthesizes text replies back into audio
4. Extracts structured data from photographed documents
5. Orchestrates all steps behind a single CLI or HTTP interface

---

## 1. Project Skeleton & Repository Layout

Create the following top-level folders and files:

```
receptro-ai-pipeline/
├── transcribe/         # Speech-to-text logic & tests
│   ├── transcribe.py
│   ├── tests/
│   └── requirements.txt
├── interpret/          # NLU intent/parameter extraction
│   ├── interpret.py
│   ├── models/
│   └── requirements.txt
├── synthesize/         # Text-to-speech synthesis
│   ├── synthesize.py
│   ├── voices/
│   └── requirements.txt
├── extract/            # OCR & structured field extraction
│   ├── extract.py
│   ├── templates/
│   └── requirements.txt
├── orchestrator/       # CLI or HTTP server
│   ├── app.py
│   ├── config.yaml
│   ├── Dockerfile      # Optional automated runner
│   └── requirements.txt
├── samples/            # Test inputs & expected outputs
│   ├── sample.wav
│   └── doc.png
├── outputs/            # Generated JSON & audio outputs
│   ├── sample.json
│   ├── reply.wav
│   └── doc.json
├── README.md           # Usage instructions and design rationale
└── .gitignore
```

## 1.1 Recommended Technology Stack

* **Language & Runtime:** Python 3.9+ (widely adopted, extensive libraries)
* **Audio Processing & Transcription:** OpenAI Whisper (`whisper` library) or Google Cloud Speech-to-Text (`google-cloud-speech`), with `pydub` for audio I/O
* **NLU & Intent Parsing:** OpenAI GPT-4 API (`openai` SDK) or spaCy v3 (`spacy`) with rule-based matchers and `textcat`
* **Text-to-Speech Synthesis:** Amazon Polly (`boto3`) or Google Cloud Text-to-Speech (`google-cloud-texttospeech`)
* **OCR & Data Extraction:** Tesseract OCR (`pytesseract`) or AWS Textract (`boto3`), plus `opencv-python` for image preprocessing
* **Orchestrator & Interface:** FastAPI with Uvicorn for HTTP endpoints or Typer/Click for CLI workflows
* **Containerization & Automation:** Docker and Docker Compose for environment consistency
* **Configuration Management:** Pydantic (`pydantic`) for schema validation and `PyYAML` for `config.yaml` parsing
* **Testing & Quality:** PyTest (`pytest`) for unit tests; pre-commit hooks (`pre-commit`) for linting and formatting

Each submodule (`transcribe/`, `interpret/`, etc.) should include:

Each submodule (`transcribe/`, `interpret/`, etc.) should include:

* Core implementation file (e.g., `transcribe.py`)
* A lightweight test suite (`tests/`) demonstrating expected behavior
* A `requirements.txt` declaring dependencies

---

## 2. Task Breakdown & Tracking

### 2.1 Define High-Level Tasks

1. **T1: Setup Project Structure**
2. **T2: Implement Speech-to-Text**
3. **T3: Implement Intent Extraction**
4. **T4: Implement Text-to-Speech**
5. **T5: Implement Document OCR & Extraction**
6. **T6: Build Orchestrator Interface (CLI/HTTP)**
7. **T7: Write README & Configuration Guide**
8. **T8: Write Automated Runner (Bonus)**

### 2.2 Chunk Each High-Level Task into Subtasks

#### T1: Setup Project Structure

* T1.1 Create repository and initialize Git
* T1.2 Create each folder and stub files
* T1.3 Add `.gitignore` and base `requirements.txt`
* T1.4 Verify folder structure locally

#### T2: Implement Speech-to-Text

* T2.1 Select transcription engine (e.g., OpenAI Whisper, Google Speech-to-Text)
* T2.2 Write `transcribe.transcribe_audio(input_path)` to return raw text
* T2.3 Write unit tests for sample WAV file
* T2.4 Handle errors (e.g., unsupported format, engine failures)
* T2.5 Generate output JSON schema (`text`, `confidence`, `timestamps`)

#### T3: Implement Intent Extraction

* T3.1 Choose NLU library (e.g., Rasa, spaCy, OpenAI GPT)
* T3.2 Define intent schema and parameter definitions
* T3.3 Write `interpret.parse_intent(text)` to return structured JSON (`intent`, `params`)
* T3.4 Train or configure models if required
* T3.5 Write tests with sample sentences

#### T4: Implement Text-to-Speech

* T4.1 Select TTS engine (e.g., Amazon Polly, Google TTS, OpenAI TTS)
* T4.2 Write `synthesize.text_to_speech(text, voice)` to emit `reply.wav`
* T4.3 Support configuration of voice, speed, and format
* T4.4 Write unit tests for short text replies

#### T5: Implement OCR & Extraction

* T5.1 Choose OCR engine (e.g., Tesseract, AWS Textract)
* T5.2 Define document field mapping (e.g., name, date, ID)
* T5.3 Write `extract.parse_document(image_path)` to return JSON fields
* T5.4 Write template-based or ML-based extraction logic in `templates/`
* T5.5 Write tests using `doc.png` sample

#### T6: Build Orchestrator Interface

* T6.1 Decide on CLI or HTTP interface (or both)
* T6.2 Use `argparse` for CLI or Flask/FastAPI for HTTP
* T6.3 Implement file type detection (`.wav`, `.png`, `.jpg`, `.txt`)
* T6.4 Auto-route to respective module and gather outputs
* T6.5 Return or print final JSON and any media files
* T6.6 Add logging and configuration support via `config.yaml`

#### T7: Write README & Configuration Guide

* T7.1 Document how to install dependencies per module
* T7.2 Show CLI and HTTP example commands
* T7.3 Explain design decisions and swapping engines
* T7.4 Provide environment variables and config overrides

#### T8: Write Automated Runner (Bonus)

* T8.1 Write a shell script or `docker-compose.yml` to stand up services
* T8.2 Ensure modules execute in sequence automatically
* T8.3 Add health checks and sample dataset execution
* T8.4 Document runner in README

---

## 3. Task Tracking Table

Maintain a `TASKS.md` file with the following template:

| ID   | Task Description              | Owner | Status      | Notes                      |
| ---- | ----------------------------- | ----- | ----------- | -------------------------- |
| T1   | Setup Project Structure       | Agent | ✅ Completed | Base structure in place    |
| T2   | Implement Speech-to-Text      | Agent | In Progress | Whisper integration chosen |
| T2.1 | - Select transcription engine | Agent | ✅ Completed | OpenAI Whisper             |
| T2.2 | - Write transcribe.py         | Agent | ✅ Completed |                            |
| ...  | ...                           | ...   | ...         | ...                        |

Update this file as tasks progress.

---

## 4. Running the End-to-End Flow

### 4.1 CLI Example

```bash
# Transcribe audio
python orchestrator/app.py process --file samples/sample.wav --output outputs/sample.json

# OCR document
python orchestrator/app.py process --file samples/doc.png --output outputs/doc.json
```

### 4.2 HTTP Example (if implemented)

```bash
curl -X POST http://localhost:8000/process \
  -F file=@samples/sample.wav \
  -o outputs/sample_response.json
```

---

## 5. Swapping Engines & Extensibility

### Transcription

* To use Google Speech-to-Text: update `transcribe/requirements.txt` and import `google.cloud.speech`
* Change function reference in `transcribe.py` and `config.yaml`

### NLU Interpretation

* To use Rasa: add Rasa project in `interpret/models/` and update `interpret.py`

### Synthesis

* To use Amazon Polly: install `boto3`, configure AWS creds, update `synthesize.py`

### OCR Extraction

* To use AWS Textract: install `boto3`, update `extract.py` to call Textract API

---

## 6. Assumptions & Clarifications

* Audio files < 10s, mono WAV/MP3, 16kHz sample rate
* Documents are printed (not handwriting), minimum resolution 300 DPI
* Docker Compose runner uses local modules; no external services required

---

*End of Instructions Document*
