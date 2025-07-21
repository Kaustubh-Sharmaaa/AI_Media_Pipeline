import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from synthesize.synth import text_to_speech


def test_text_to_speech_creates_file():
    output_path = os.path.join('outputs', 'test_reply.wav')
    text = "This is a test reply from the car showroom assistant."
    result_path = text_to_speech(text, output_path=output_path)
    assert os.path.isfile(result_path)
    assert os.path.getsize(result_path) > 1000  # Should not be empty
    os.remove(result_path) 