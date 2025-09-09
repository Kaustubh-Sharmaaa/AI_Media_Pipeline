import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from transcribe import transcribe


def test_transcribe_stub_present():
    # Basic sanity check that module imports and has function
    assert hasattr(transcribe, 'transcribe_audio')
