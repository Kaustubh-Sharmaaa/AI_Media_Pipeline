import typer
import os
import json
from typing import Optional

app = typer.Typer(help="""
AI Media Pipeline CLI Orchestrator

Usage Examples:
  python -m ai_media_pipeline.orchestrator.app process --file samples/input.wav --output outputs/input.json
  python -m ai_media_pipeline.orchestrator.app process --file registration_document.png --output outputs/registration.json
  python -m ai_media_pipeline.orchestrator.app process --file samples/sample.txt --output outputs/reply.wav
""")

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
            from ai_media_pipeline.transcribe.transcribe import transcribe_audio
            from ai_media_pipeline.interpret.interpret import parse_intent
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
            from ai_media_pipeline.extract.extract import parse_document
            result = parse_document(file)
            typer.echo(f"[Extracted Fields] {json.dumps(result, indent=2)}")
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            typer.echo(f"[DEBUG] Output written to {output}")
        elif ext in ['.txt']:
            typer.echo("[DEBUG] Detected text file. Running intent extraction and TTS...")
            from ai_media_pipeline.interpret.interpret import parse_intent
            from ai_media_pipeline.synthesize.synth import text_to_speech
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

if __name__ == "__main__":
    app()
