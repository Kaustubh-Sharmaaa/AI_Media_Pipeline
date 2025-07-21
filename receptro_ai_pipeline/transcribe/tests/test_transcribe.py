import os
import sys
import pytest

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from transcribe.transcribe import transcribe_audio

SAMPLE_AUDIO = os.path.join(os.path.dirname(__file__), "..", "..", "samples", "sample.wav")


def test_transcribe_audio_success():
    if not os.path.isfile(SAMPLE_AUDIO):
        pytest.skip("Sample audio file not found.")
    result = transcribe_audio(SAMPLE_AUDIO)
    assert isinstance(result, dict)
    assert "text" in result
    assert "confidence" in result
    assert "timestamps" in result
    assert isinstance(result["text"], str)
    assert isinstance(result["confidence"], float)
    assert isinstance(result["timestamps"], list)


def test_transcribe_audio_file_not_found():
    with pytest.raises(FileNotFoundError):
        transcribe_audio("nonexistent.wav")


def test_transcribe_audio_unsupported_format():
    with pytest.raises(ValueError):
        transcribe_audio("file.txt") 