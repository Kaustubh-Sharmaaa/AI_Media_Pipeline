import pytesseract
import cv2
import re
import os
from typing import Dict, Any

def parse_document(image_path: str) -> Dict[str, Any]:
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image file.")
    # Convert to grayscale and apply threshold for better OCR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # OCR
    text = pytesseract.image_to_string(thresh)
    # Extract fields using regex (customize as needed)
    fields = {}
    # Name (e.g., Name: John Doe)
    m = re.search(r"Name[:\s]+([A-Za-z ]+)", text)
    if m:
        fields["name"] = m.group(1).strip()
    # Registration Number (e.g., Reg No: ABC1234)
    m = re.search(r"Reg(?:istration)? No[:\s]+([A-Z0-9]+)", text, re.I)
    if m:
        fields["registration_number"] = m.group(1).strip()
    # Car Make (e.g., Make: Ford)
    m = re.search(r"Make[:\s]+([A-Za-z]+)", text)
    if m:
        fields["car_make"] = m.group(1).strip()
    # Car Model (e.g., Model: Mustang GT)
    m = re.search(r"Model[:\s]+([A-Za-z0-9 ]+)", text)
    if m:
        fields["car_model"] = m.group(1).strip()
    # Date (e.g., Date: 2024-07-20)
    m = re.search(r"Date[:\s]+([0-9\-/]+)", text)
    if m:
        fields["date"] = m.group(1).strip()
    # Add raw text for reference
    fields["raw_text"] = text
    return fields 