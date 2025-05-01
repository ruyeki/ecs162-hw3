import backend.app as app
from unittest.mock import patch, Mock
import requests
from dotenv import load_dotenv
import os

load_dotenv()
nyt_api_key = os.getenv('NYT_API_KEY')


#Test the api key and ensure that the flask server returns it
def test_api_key_present(): 
    assert nyt_api_key is not None

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
   
def test_api(): 
    url =  'https://api.nytimes.com/svc/search/v2/articlesearch.json'

    params = {
        'q': 'Davis (Calif) AND Sacramento (Calif))',
        'api-key': nyt_api_key 
    }

    response = requests.get(url, params=params)

    #validate status code
    assert response.status_code == 200

    data = response.json()

    #Validate the json
    assert "response" in data 
    assert "docs" in data["response"]

    #since docs contains a list of articles, ensure that it is a valid list
    assert isinstance(data["response"]["docs"], list)

    story = data["response"]["docs"][0]

    #Validate the format of the api response

    #Make sure the title is correctly there
    assert "headline" in story and "main" in story["headline"]

    #Make sure multimedia is there
    assert "multimedia" in story

    #Make sure article url is there
    assert "url" in story["multimedia"]["default"]

    #Make sure abstract is there
    assert "abstract" in story

#Test that the query is correct (returns Sac or Davis news)
def test_davis_sacramento(): 
    url =  'https://api.nytimes.com/svc/search/v2/articlesearch.json'

    params = {
        'q': 'Davis (Calif) AND Sacramento (Calif))',
        'api-key': nyt_api_key 
    }

    response = requests.get(url, params=params)

    #validate status code
    assert response.status_code == 200

    data = response.json()

    #Validate the json
    assert "response" in data 
    assert "docs" in data["response"]

    #since docs contains a list of articles, ensure that it is a valid list
    assert isinstance(data["response"]["docs"], list)

    story = data["response"]["docs"]

    article_valid = False

    for article in story: 
        headline = article["headline"]["main"]

        if ("davis" or "Davis" in headline) or ("sacramento" or "Sacramento" in headline): 
            article_valid = True
            break
    
    assert article_valid, "Cannot find relevant articles"