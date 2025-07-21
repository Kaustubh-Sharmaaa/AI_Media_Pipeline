import typer
import os
import json
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
import uvicorn

app = typer.Typer(help="""
Receptro.AI CLI Orchestrator

Usage Examples:
  python -m receptro_ai_pipeline.orchestrator.app process --file samples/input.wav --output outputs/input.json
  python -m receptro_ai_pipeline.orchestrator.app process --file registration_document.png --output outputs/registration.json
  python -m receptro_ai_pipeline.orchestrator.app process --file samples/sample.txt --output outputs/reply.wav
  python -m receptro_ai_pipeline.orchestrator.app serve  # Launch HTTP API (see docs below)

HTTP API:
  POST /process
    - file: (form-data) audio, image, or text file
    - voice: (optional, for TTS)
    - rate: (optional, for TTS)
    Returns: JSON (for audio/image) or WAV file (for TTS)
""")

fastapi_app = FastAPI(title="Receptro.AI Orchestrator API")

@fastapi_app.get("/", response_class=HTMLResponse)
async def root_ui():
    return """
    <html>
    <head>
      <title>Receptro.AI Sequential Pipeline Demo</title>
      <style>
        body { font-family: Arial, sans-serif; background: #f6f8fa; margin: 0; padding: 0; }
        .container { max-width: 600px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #0001; padding: 32px; }
        h2 { text-align: center; color: #2d3a4a; }
        ol { padding-left: 20px; }
        li { margin-bottom: 32px; }
        form { margin-bottom: 8px; }
        textarea { width: 100%; font-size: 1em; border-radius: 6px; border: 1px solid #ccc; padding: 8px; }
        input[type='file'] { margin-bottom: 8px; }
        button { background: #2563eb; color: #fff; border: none; border-radius: 6px; padding: 8px 16px; font-size: 1em; cursor: pointer; transition: background 0.2s; }
        button:disabled { background: #b3c6e0; cursor: not-allowed; }
        .step-title { font-weight: bold; color: #2563eb; }
        .output-card { background: #f1f5fb; border-radius: 8px; padding: 12px; margin-top: 8px; font-size: 0.98em; overflow-x: auto; }
        .loading { color: #eab308; font-weight: bold; }
        pre, code { white-space: pre-wrap; word-break: break-word; font-family: inherit; }
      </style>
    </head>
    <body>
      <div class="container">
      <h2>Receptro.AI Pipeline: Sequential Demo</h2>
      <ol>
        <li><span class="step-title">1. Speech-to-Text & Intent Extraction</span><br>
          <form id='stt-form' enctype='multipart/form-data'>
            <input type='file' name='file' accept='.wav,.mp3,.m4a,.flac,.ogg' required>
            <button type='submit'>Transcribe & Interpret</button>
          </form>
          <div id='stt-loading' class='loading' style='display:none;'>Loading...</div>
          <div id='stt-output' class='output-card'></div>
        </li>
        <li><span class="step-title">2. Document OCR & Extraction</span><br>
          <form id='ocr-form' enctype='multipart/form-data'>
            <input type='file' name='file' accept='.png,.jpg,.jpeg' required disabled>
            <button type='submit' disabled>Extract Fields</button>
          </form>
          <div id='ocr-loading' class='loading' style='display:none;'>Loading...</div>
          <div id='ocr-output' class='output-card'></div>
        </li>
        <li><span class="step-title">3. Generate & Download Audio Reply</span><br>
          <form id='reply-form'>
            <textarea id='reply-text' name='text' rows='3' cols='60' placeholder='Summary reply will appear here...'></textarea><br>
            <button type='submit' disabled>Generate Audio Reply</button>
          </form>
          <div id='reply-loading' class='loading' style='display:none;'>Loading...</div>
          <div id='reply-output' class='output-card'></div>
        </li>
      </ol>
      </div>
      <script>
        let sttData = null;
        let ocrData = null;
        // Step 1: Speech-to-Text & Intent
        document.getElementById('stt-form').onsubmit = async (e) => {
          e.preventDefault();
          document.getElementById('stt-loading').style.display = 'block';
          document.getElementById('stt-output').innerHTML = '';
          const formData = new FormData(e.target);
          const res = await fetch('/process', { method: 'POST', body: formData });
          const data = await res.json();
          console.log('[STT] Raw response:', data);
          document.getElementById('stt-loading').style.display = 'none';
          if (data.transcription && data.intent) {
            sttData = data; // Assign data to sttData for later use
            document.getElementById('stt-output').innerHTML =
              '<b>Transcription:</b><pre>' + JSON.stringify(data.transcription, null, 2) + '</pre>' +
              '<b>Intent:</b><pre>' + JSON.stringify(data.intent, null, 2) + '</pre>';
            // Enable OCR step
            const ocrInputs = document.querySelectorAll('#ocr-form input, #ocr-form button');
            ocrInputs.forEach(el => el.disabled = false);
          } else if (data.error) {
            document.getElementById('stt-output').innerHTML = '<span style="color:red;">Error: ' + data.error + '</span>';
            console.error('[STT] Error:', data.error);
          } else {
            document.getElementById('stt-output').innerHTML = '<span style="color:red;">Unexpected response: ' + JSON.stringify(data) + '</span>';
            console.error('[STT] Unexpected response:', data);
          }
        };
        // Step 2: OCR
        document.getElementById('ocr-form').onsubmit = async (e) => {
          e.preventDefault();
          document.getElementById('ocr-loading').style.display = 'block';
          document.getElementById('ocr-output').innerHTML = '';
          const formData = new FormData(e.target);
          const res = await fetch('/process', { method: 'POST', body: formData });
          ocrData = await res.json();
          console.log('[OCR] Raw response:', ocrData);
          document.getElementById('ocr-loading').style.display = 'none';
          document.getElementById('ocr-output').innerHTML = '<pre>' + JSON.stringify(ocrData, null, 2) + '</pre>';
          // Enable reply step and auto-generate summary
          const replyBtn = document.querySelector('#reply-form button');
          replyBtn.disabled = false;
          // Compose summary
          let summary = '';
          if (sttData && sttData.intent && sttData.intent.params) {
            const p = sttData.intent.params;
            summary += `You asked about the ${p.car_make || ''} ${p.car_model || ''}`;
            if (ocrData && ocrData.text) {
              // Try to extract fields from OCR text
              const regMatch = ocrData.text.match(/Registration No\\.:?\\s*([A-Za-z0-9]+)/i);
              const ownerMatch = ocrData.text.match(/Name:?\\s*([A-Za-z .]+)/i);
              summary += regMatch ? `, registration number ${regMatch[1]}` : '';
              summary += ownerMatch ? `, owned by ${ownerMatch[1]}` : '';
            }
            summary += '.';
          } else {
            summary = 'Unable to generate summary.';
            console.error('[SUMMARY] Could not generate summary. sttData:', sttData, 'ocrData:', ocrData);
          }
          document.getElementById('reply-text').value = summary;
        };
        // Step 3: Generate Audio Reply
        document.getElementById('reply-form').onsubmit = async (e) => {
          e.preventDefault();
          document.getElementById('reply-loading').style.display = 'block';
          document.getElementById('reply-output').innerHTML = '';
          const text = document.getElementById('reply-text').value;
          const formData = new FormData();
          const blob = new Blob([text], { type: 'text/plain' });
          formData.append('file', blob, 'input.txt');
          const res = await fetch('/process', { method: 'POST', body: formData });
          console.log('[TTS] Response headers:', res.headers);
          document.getElementById('reply-loading').style.display = 'none';
          if (res.headers.get('content-type').includes('audio/wav')) {
            const audioBlob = await res.blob();
            const url = URL.createObjectURL(audioBlob);
            document.getElementById('reply-output').innerHTML = `<a href="${url}" download="reply.wav">Download reply.wav</a>`;
          } else {
            document.getElementById('reply-output').innerText = 'TTS failed.';
            try {
              const err = await res.json();
              console.error('[TTS] Error:', err);
            } catch (e) {
              console.error('[TTS] Unknown error');
            }
          }
        };
      </script>
    </body>
    </html>
    """

@fastapi_app.post("/process")
async def process_api(
    file: UploadFile = File(...),
    voice: Optional[str] = Form(None),
    rate: Optional[str] = Form(None)  # Accept as string
):
    import tempfile
    import shutil
    import traceback
    ext = os.path.splitext(file.filename)[1].lower()
    print(f"[API] Received file: {file.filename} (ext: {ext})")
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        if ext in ['.wav', '.mp3', '.m4a', '.flac', '.ogg']:
            print(f"[API] Detected audio file. Running transcription...")
            from receptro_ai_pipeline.transcribe.transcribe import transcribe_audio
            from receptro_ai_pipeline.interpret.interpret import parse_intent
            result = transcribe_audio(tmp_path)
            print(f"[API] Transcription result: {result}")
            nlu = parse_intent(result['text'])
            print(f"[API] Intent extraction result: {nlu}")
            return JSONResponse(content={'transcription': result, 'intent': nlu})
        elif ext in ['.png', '.jpg', '.jpeg']:
            print(f"[API] Detected image file. Running OCR extraction...")
            from receptro_ai_pipeline.extract.extract import parse_document
            result = parse_document(tmp_path)
            print(f"[API] OCR result: {result}")
            return JSONResponse(content=result)
        elif ext in ['.txt']:
            print(f"[API] Detected text file. Running intent extraction and TTS...")
            rate_val = int(rate) if rate and rate.strip() else None
            from receptro_ai_pipeline.interpret.interpret import parse_intent
            from receptro_ai_pipeline.synthesize.synth import text_to_speech
            with open(tmp_path) as f:
                text = f.read()
            print(f"[API] Text for TTS: {text}")
            nlu = parse_intent(text)
            print(f"[API] Intent extraction result: {nlu}")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as out_tmp:
                wav_path = text_to_speech(text, voice=voice, rate=rate_val, output_path=out_tmp.name)
            print(f"[API] TTS output path: {wav_path}")
            headers = {"X-Intent": json.dumps(nlu)}
            return FileResponse(wav_path, media_type="audio/wav", filename="reply.wav", headers=headers)
        else:
            print(f"[API] Unsupported file type: {ext}")
            return JSONResponse(content={"error": "Unsupported file type."}, status_code=400)
    except Exception as e:
        print(f"[API] Exception occurred: {e}")
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        os.remove(tmp_path)

@app.command()
def process(
    file: str = typer.Option(..., '--file', '-f', help='Input file path (.wav, .png, .txt)'),
    output: str = typer.Option(..., '--output', '-o', help='Output file path (JSON or WAV)'),
    voice: Optional[str] = typer.Option(None, '--voice', help='Voice for TTS'),
    rate: Optional[int] = typer.Option(None, '--rate', help='Speech rate for TTS'),
):
    """
    Process an input file (audio, image, or text) and output the result.
    """
    typer.echo(f"[DEBUG] Starting process for file: {file} -> {output}")
    ext = os.path.splitext(file)[1].lower()
    try:
        if ext in ['.wav', '.mp3', '.m4a', '.flac', '.ogg']:
            typer.echo("[DEBUG] Detected audio file. Running transcription...")
            from receptro_ai_pipeline.transcribe.transcribe import transcribe_audio
            from receptro_ai_pipeline.interpret.interpret import parse_intent
            result = transcribe_audio(file)
            typer.echo(f"[Transcription] {result['text']}")
            typer.echo("[DEBUG] Running intent extraction...")
            nlu = parse_intent(result['text'])
            typer.echo(f"[Intent] {json.dumps(nlu, indent=2)}")
            with open(output, 'w') as f:
                json.dump({'transcription': result, 'intent': nlu}, f, indent=2)
            typer.echo(f"[DEBUG] Output written to {output}")
        elif ext in ['.png', '.jpg', '.jpeg']:
            typer.echo("[DEBUG] Detected image file. Running OCR extraction...")
            from receptro_ai_pipeline.extract.extract import parse_document
            result = parse_document(file)
            typer.echo(f"[Extracted Fields] {json.dumps(result, indent=2)}")
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            typer.echo(f"[DEBUG] Output written to {output}")
        elif ext in ['.txt']:
            typer.echo("[DEBUG] Detected text file. Running intent extraction and TTS...")
            from receptro_ai_pipeline.interpret.interpret import parse_intent
            from receptro_ai_pipeline.synthesize.synth import text_to_speech
            with open(file) as f:
                text = f.read()
            nlu = parse_intent(text)
            typer.echo(f"[Intent] {json.dumps(nlu, indent=2)}")
            wav_path = text_to_speech(text, voice=voice, rate=rate, output_path=output)
            typer.echo(f"[DEBUG] Audio reply written to {wav_path}")
        else:
            typer.echo("[ERROR] Unsupported file type.", err=True)
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"[ERROR] Exception occurred: {e}", err=True)
        raise typer.Exit(1)

@app.command()
def serve():
    """Run the HTTP API server (FastAPI) on http://0.0.0.0:8000"""
    typer.echo("[INFO] Starting FastAPI server on http://0.0.0.0:8000 ...")
    uvicorn.run("receptro_ai_pipeline.orchestrator.app:fastapi_app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    app()
