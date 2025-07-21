import pyttsx3
import os
from typing import Optional

def text_to_speech(text: str, voice: Optional[str] = None, rate: Optional[int] = None, output_path: str = "output.wav") -> str:
    """
    Synthesize speech from text and save to output_path (WAV).
    """
    engine = pyttsx3.init()
    # Set voice
    selected_voice = None
    try:
        voices = engine.getProperty('voices')
        if voice:
            for v in voices:
                if voice.lower() in v.id.lower() or voice.lower() in v.name.lower():
                    engine.setProperty('voice', v.id)
                    selected_voice = v.id
                    break
            if not selected_voice:
                print(f"[TTS] Requested voice '{voice}' not found. Using default.")
        else:
            # Try to set to English if not specified
            for v in voices:
                if 'en' in v.id or 'english' in v.name.lower():
                    engine.setProperty('voice', v.id)
                    selected_voice = v.id
                    break
            if not selected_voice:
                print("[TTS] No English voice found. Using system default.")
    except Exception as e:
        print(f"[TTS] Error setting voice: {e}. Proceeding with default voice.")
    if rate:
        try:
            engine.setProperty('rate', rate)
        except Exception as e:
            print(f"[TTS] Error setting rate: {e}")
    if output_path is None:
        output_path = "output.wav"
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path
