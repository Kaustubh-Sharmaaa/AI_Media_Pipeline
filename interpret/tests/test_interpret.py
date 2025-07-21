import sys
import os
import pytest
from interpret.interpret import parse_intent
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



def test_parse_intent_sample():
    text = "Hi, I would like to get information about the car that I checked out yesterday. The Ford Mustang GT which was in red."
    result = parse_intent(text)
    assert result["intent"] == "get_information"
    assert result["params"]["car_make"] == "Ford"
    assert result["params"]["car_model"] == "Mustang GT"
    assert result["params"]["color"] == "red"
    assert result["params"]["date"] == "yesterday"

def test_parse_intent_test_drive():
    text = "Can I book a test drive for the blue BMW X5 tomorrow?"
    result = parse_intent(text)
    assert result["intent"] == "book_test_drive"
    assert result["params"]["car_make"] == "BMW"
    assert result["params"]["car_model"] == "X5"
    assert result["params"]["color"] == "blue"
    assert result["params"]["date"] == "tomorrow"

def test_parse_intent_no_color():
    text = "Tell me about the Toyota Corolla."
    result = parse_intent(text)
    assert result["intent"] == "get_information"
    assert result["params"]["car_make"] == "Toyota"
    assert result["params"]["car_model"] == "Corolla"
    assert "color" not in result["params"]

def test_parse_intent_unknown():
    text = "I want something fast."
    result = parse_intent(text)
    assert result["intent"] == "unknown"
    assert result["params"] == {} 