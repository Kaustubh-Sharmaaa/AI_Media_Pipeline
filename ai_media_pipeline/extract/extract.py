import pytesseract
from PIL import Image
from typing import Dict, Any
import os

def parse_document(image_path: str) -> Dict[str, Any]:
    """
    Perform OCR on the given image and return a dict with the extracted text.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return {"text": text}
    except Exception as e:
        raise RuntimeError(f"OCR failed: {e}")
