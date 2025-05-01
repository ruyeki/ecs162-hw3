import app
from unittest.mock import patch, Mock


#Comprehensive testing for extract_city_from_keywords function
def test_extract_city_from_keywords_sacramento():
    assert app.extract_city_from_keywords([{"value": "Sacramento"}]) == "Sacramento"

def test_extract_city_from_keywords_davis(): 
    assert app.extract_city_from_keywords([{"value": "City of Davis"}]) == "Davis"

def test_extract_city_from_keywords_none(): 
    assert app.extract_city_from_keywords([{"value": "Los Angeles"}]) is None

def test_extract_city_from_keywords_empty(): 
    assert app.extract_city_from_keywords([{"value": ""}]) is None

def test_extract_city_from_keywords_case_insensitive(): 
    assert app.extract_city_from_keywords([{"value": "SaCraMento"}]) == "Sacramento"






#Still in progress
def test_get_stories(): 
    assert app.get_stories()
