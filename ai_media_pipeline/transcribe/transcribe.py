import whisper
import os
from typing import Dict, Any


def transcribe_audio(input_path: str) -> Dict[str, Any]:
    """
    Transcribe an audio file using OpenAI Whisper.
    Returns a dict: { 'text': str, 'confidence': float, 'timestamps': list }
    """
    if not input_path.lower().endswith((".wav", ".mp3", ".m4a", ".flac", ".ogg")):
        raise ValueError("Unsupported audio format. Supported: wav, mp3, m4a, flac, ogg")
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")
    try:
        model = whisper.load_model("base")
        result = model.transcribe(input_path, word_timestamps=True)
        text = result.get("text", "")
        segments = result.get("segments", [])
        # Calculate average confidence and collect timestamps
        confidences = [seg.get("avg_logprob", 0.0) for seg in segments if "avg_logprob" in seg]
        # Whisper's avg_logprob is log-probability; convert to [0,1] scale for confidence
        confidence = float(sum(confidences) / len(confidences)) if confidences else 0.0
        confidence = min(max((confidence + 5) / 10, 0.0), 1.0)  # crude normalization
        timestamps = [
            {"start": seg["start"], "end": seg["end"], "text": seg["text"]}
            for seg in segments
        ]
        return {"text": text, "confidence": confidence, "timestamps": timestamps}
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {e}")
