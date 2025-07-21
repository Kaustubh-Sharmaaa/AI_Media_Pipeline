import pyttsx3
import os
from typing import Optional

def text_to_speech(text: str, voice: Optional[str] = None, rate: Optional[int] = None, output_path: str = 'outputs/reply.wav') -> str:
    """
    Synthesize speech from text and save to output_path (WAV).
    Optionally set voice and rate.
    Returns the path to the generated audio file.
    """
    engine = pyttsx3.init()
    if voice:
        for v in engine.getProperty('voices'):
            if voice.lower() in v.name.lower():
                engine.setProperty('voice', v.id)
                break
    if rate:
        engine.setProperty('rate', rate)
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path 