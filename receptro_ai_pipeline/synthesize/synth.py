import pyttsx3
import os
from typing import Optional

def text_to_speech(text: str, voice: Optional[str] = None, rate: Optional[int] = None, output_path: str = "output.wav") -> str:
    """
    Synthesize speech from text and save to output_path (WAV).
    """
    engine = pyttsx3.init()
    if voice:
        for v in engine.getProperty('voices'):
            if voice.lower() in v.name.lower():
                engine.setProperty('voice', v.id)
                break
    if rate:
        engine.setProperty('rate', rate)
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path
