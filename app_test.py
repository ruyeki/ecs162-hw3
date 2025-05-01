import app
from unittest.mock import patch, Mock

def test_extract_city_from_keywords():
    assert app.extract_city_from_keywords([{"value": "Sacramento"}]) == "Sacramento"

#Still in progress
def test_get_stories(): 
    assert app.get_stories()
