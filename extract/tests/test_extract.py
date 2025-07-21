import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from extract.extract import parse_document


def test_parse_document_fields():
    sample_path = os.path.join('samples', '..', 'registration_document.png')
    if not os.path.isfile(sample_path):
        pytest.skip("Sample registration document not found.")
    result = parse_document(sample_path)
    assert isinstance(result, dict)
    assert "raw_text" in result
    # At least one field should be present besides raw_text
    assert any(k for k in result if k != "raw_text") 