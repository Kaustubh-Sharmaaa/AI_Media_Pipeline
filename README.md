# AI Media & Data Processing Pipeline

---

## 🚀 Project Overview

This repository is a showcase of my ability to design, implement, debug, and deliver a **production-grade, modular AI pipeline** for real-world media and data processing. It demonstrates:
- **Full-stack engineering:** From Python modules to Docker orchestration
- **AI/ML integration:** Speech-to-text, NLU, TTS, and OCR
- **Robust debugging and problem-solving**
- **Best practices:** Modularization, documentation, reproducibility, and automation

**Why this project matters:**
- It covers the full lifecycle: requirements analysis, architecture, implementation, testing, containerization, and documentation.
- It integrates multiple AI technologies and open-source tools, showing my ability to work across domains.
- The codebase is clean, well-structured, and ready for extension or production use.
- The README and commit history transparently document my engineering process, challenges, and solutions.
- It is designed to be run by anyone, anywhere, with minimal setup—just clone and run in Docker.

---

## 📚 Case Study: Example End-to-End Flow

### Scenario
A customer at a car showroom wants to know more about a specific car they saw yesterday. They use a voice interface to ask:

> "Hi, I would like to get information about the car that I checked out yesterday. The Ford Mustang GT which was in red."

### Step 1: Audio Input
- The user records their query as `input.wav` and uploads it to the system.

### Step 2: Pipeline Processing (via Docker)
```sh
docker run --rm \
  -v $(pwd)/ai_media_pipeline/samples:/app/ai_media_pipeline/samples \
  -v $(pwd)/ai_media_pipeline/outputs:/app/ai_media_pipeline/outputs \
  ai-media-pipeline \
  --file ai_media_pipeline/samples/input.wav \
  --output ai_media_pipeline/outputs/input.json
```

### Step 3: What Happens Internally
- **Transcription:** The audio is transcribed using OpenAI Whisper.
- **Intent Extraction:** The transcribed text is analyzed with spaCy to extract the user's intent and parameters (car make, model, color, date).
- **Output:** The results are saved as a JSON file.

### Step 4: Output Example
The output file `outputs/input.json` contains:
```json
{
  "transcription": {
    "text": "Hi, I would like to get information about the car that I checked out yesterday. The Ford Mustang GT which was in red.",
    "confidence": 0.98,
    "timestamps": [
      {"start": 0.0, "end": 2.5, "text": "Hi, I would like to get information..."},
      {"start": 2.5, "end": 5.0, "text": "...about the car that I checked out yesterday."},
      {"start": 5.0, "end": 7.0, "text": "The Ford Mustang GT which was in red."}
    ]
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

### Step 5: How This Helps
- The sales team or an automated system can now instantly respond with detailed information about the specific car the customer is interested in, without manual data entry or ambiguity.
- This same pipeline can handle document images (for OCR) and text queries (for TTS), making it a versatile, real-world AI solution.

---

## 🛠️ Development Journey, Debugging & Challenges

### **1. Initial Planning & Architecture**
- Broke down requirements into modular subprojects: transcribe, interpret, synthesize, extract, orchestrator.
- Designed a clear folder structure for separation of concerns and easy extensibility.

### **2. Implementation**
- Implemented each module with a focus on single responsibility and testability.
- Used OpenAI Whisper for robust speech-to-text, spaCy for intent extraction, pyttsx3 for TTS, and pytesseract for OCR.
- Created a Typer-based CLI for unified orchestration.

### **3. Debugging & Problem Solving**
- **Dependency hell:** Resolved conflicts between system and Python dependencies (e.g., Whisper, spaCy, Tesseract, pyttsx3, build tools).
- **Whisper confusion:** Fixed issues with the wrong `whisper` package by installing from GitHub, not PyPI.
- **spaCy model:** Automated download of `en_core_web_sm` in Docker.
- **Docker context:** Moved Dockerfile to project root for correct build context and volume mounting.
- **Build failures:** Added `build-essential` and `git` to Dockerfile to support all dependencies.
- **Logging:** Added echo statements in Dockerfile and debug logs in Python for transparency.
- **Testing:** Validated all flows (audio, image, text) both locally and in Docker.

### **4. Documentation & Reproducibility**
- Wrote detailed, step-by-step README and in-code comments.
- Maintained a development log and checklist for transparency.
- Ensured all steps, fixes, and design decisions are documented for future contributors and hiring managers.

### **5. Challenges Faced**
- Integrating multiple AI/ML libraries with different system requirements.
- Ensuring the pipeline works identically in local and containerized environments.
- Making the project truly plug-and-play for anyone, regardless of OS or Python experience.
- Balancing modularity with ease of use and clear orchestration.

---

## 💡 Why This Project Demonstrates Strong Engineering Skills
- **End-to-end delivery:** From requirements to a working, documented, and containerized solution.
- **AI/ML integration:** Shows ability to work with modern AI libraries and APIs.
- **Debugging:** Overcame real-world dependency and build issues, documented solutions.
- **Automation:** Docker and Compose make the project reproducible and portable.
- **Communication:** README and commit history are clear, detailed, and professional.
- **Extensibility:** The codebase is ready for new features (e.g., HTTP API, advanced OCR, cloud deployment).

---

## 🚦 How to Use This Project (Quick Start)

### 🏁 **Quick Start (Docker)**
1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd AI_Media_Pipeline
   ```
2. **Build the Docker image:**
   ```sh
   docker build -t ai-media-pipeline .
   ```
3. **Run a sample pipeline (audio to JSON):**
   ```sh
   docker run --rm \
     -v $(pwd)/ai_media_pipeline/samples:/app/ai_media_pipeline/samples \
     -v $(pwd)/ai_media_pipeline/outputs:/app/ai_media_pipeline/outputs \
     ai-media-pipeline \
     --file ai_media_pipeline/samples/input.wav \
     --output ai_media_pipeline/outputs/input.json
   ```
   - The output appears in `ai_media_pipeline/outputs/input.json`.

4. **Try other file types:**
   - For OCR (image to JSON):
     ```sh
     docker run --rm -v $(pwd)/ai_media_pipeline/samples:/app/ai_media_pipeline/samples \
       -v $(pwd)/ai_media_pipeline/outputs:/app/ai_media_pipeline/outputs \
       ai-media-pipeline \
       --file ai_media_pipeline/samples/registration_document.png \
       --output ai_media_pipeline/outputs/registration.json
     ```
   - For text-to-speech (text to WAV):
     ```sh
     docker run --rm -v $(pwd)/ai_media_pipeline/samples:/app/ai_media_pipeline/samples \
       -v $(pwd)/ai_media_pipeline/outputs:/app/ai_media_pipeline/outputs \
       ai-media-pipeline \
       --file ai_media_pipeline/samples/sample.txt \
       --output ai_media_pipeline/outputs/sample_reply.wav
     ```

5. **(Optional) Use Docker Compose for easier management:**
   ```sh
   docker-compose up
   ```
   - Edit the `command:` in `docker-compose.yml` to change the input/output.

---

### 🐍 **Running Locally (Python, for advanced users)**
1. **Install Python 3.9+ and pip.**
2. **Install dependencies for each module:**
   ```sh
   pip install -r ai_media_pipeline/orchestrator/requirements.txt
   pip install -r ai_media_pipeline/transcribe/requirements.txt
   pip install -r ai_media_pipeline/interpret/requirements.txt
   pip install -r ai_media_pipeline/extract/requirements.txt
   pip install -r ai_media_pipeline/synthesize/requirements.txt
   python3 -m spacy download en_core_web_sm
   ```
3. **Run the CLI:**
   ```sh
   PYTHONPATH=. python3 ai_media_pipeline/orchestrator/app.py --file ai_media_pipeline/samples/input.wav --output ai_media_pipeline/outputs/input.json
   ```

---

### 💡 **Tips & Troubleshooting**
- **Docker not found?** Install Docker Desktop: https://www.docker.com/products/docker-desktop
- **Permission errors?** Try running with `sudo` or check your Docker permissions.
- **Output not appearing?** Make sure you are mounting the correct `outputs/` directory as a volume.
- **Want to use your own files?** Place them in `ai_media_pipeline/samples/` and adjust the `--file` and `--output` arguments.
- **Need more help?** Open an issue or check the detailed documentation below.

---

## 📥 Supported Input Types & Outputs

| File Type      | Description                | Output Type | Example Command |
|----------------|---------------------------|-------------|-----------------|
| `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg` | Audio file (speech) | JSON (transcription + intent) | `--file .../input.wav --output .../input.json` |
| `.png`, `.jpg`, `.jpeg` | Image file (document/photo) | JSON (OCR text) | `--file .../registration_document.png --output .../registration.json` |
| `.txt`         | Text file (user query)     | WAV (TTS reply) | `--file .../sample.txt --output .../sample_reply.wav` |

- All outputs are written to the `outputs/` directory (mounted as a Docker volume).
- You can add your own samples to the `samples/` directory.

---

## 🧑‍💼 For Hiring Managers & Reviewers
- This project is a **real-world demonstration** of my ability to deliver complex, production-ready AI/data solutions.
- The codebase is clean, modular, and well-documented.
- All major engineering challenges are transparently documented and solved.
- The project is ready for extension, deployment, or integration into larger systems.
- I am comfortable with both Python and DevOps (Docker, Compose, CI/CD).

If you have any questions or want to see further improvements, please reach out!

--- 

---

## Running the Web UI on Localhost with Docker

1. **Build the Docker image:**
   ```sh
   docker-compose build
   ```

2. **Start the API and Web UI:**
   ```sh
   docker-compose up api
   ```

3. **Open your browser and go to:**
   [http://localhost:8000/](http://localhost:8000/)

4. **Use the UI to:**
   - Upload an audio file for transcription and intent extraction
   - Upload an image for OCR
   - Generate and download a TTS audio reply

**Note:**
- The TTS (text-to-speech) voice quality in Docker is basic/robotic due to the use of espeak-ng. This is a known limitation of open-source TTS in containers. For better voice quality, consider using a neural TTS engine or a cloud-based service. 
