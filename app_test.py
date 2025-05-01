import app
from unittest.mock import patch, Mock
import requests


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

def test_extract_city_from_keywords_case_lower(): 
    assert app.extract_city_from_keywords([{"value": "sacramento"}]) == "Sacramento"
   


#Comprehensive testing for get_stories function
def test_get_stories(): 

    url = "https://run.mocky.io/v3/74491b46-e926-400c-9efa-4f3b242c5044"  
    response = requests.get(url)

    # Verify status code
    assert response.status_code == 200 

