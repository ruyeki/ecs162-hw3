import pytest
import backend.app as app_module
from backend.app import app, db
from backend.models import Comments
from unittest.mock import patch, Mock
import requests
from dotenv import load_dotenv
import os

from flask import url_for

load_dotenv()
nyt_api_key = os.getenv('NYT_API_KEY')


#Test the api key and ensure that the flask server returns it
def test_api_key_present(): 
    assert nyt_api_key is not None

#Comprehensive testing for extract_city_from_keywords function
def test_extract_city_from_keywords_sacramento():
    assert app_module.extract_city_from_keywords([{"value": "Sacramento"}]) == "Sacramento"

def test_extract_city_from_keywords_davis(): 
    assert app_module.extract_city_from_keywords([{"value": "City of Davis"}]) == "Davis"

def test_extract_city_from_keywords_none(): 
    assert app_module.extract_city_from_keywords([{"value": "Los Angeles"}]) is None

def test_extract_city_from_keywords_empty(): 
    assert app_module.extract_city_from_keywords([{"value": ""}]) is None

def test_extract_city_from_keywords_case_insensitive(): 
    assert app_module.extract_city_from_keywords([{"value": "SaCraMento"}]) == "Sacramento"

def test_extract_city_from_keywords_case_lower(): 
    assert app_module.extract_city_from_keywords([{"value": "sacramento"}]) == "Sacramento"
   
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

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SERVER_NAME'] = 'localhost.localdomain'

    with app.app_context():
        db.create_all()

        # Simulate a logged-in user
        test_user = app_module.User(user_id='123', username='testuser', email='test@example.com')
        app_module.users['123'] = test_user

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user'] = {'email': 'test@example.com', 'username': 'testuser'}
                sess['_user_id'] = '123'  # This is what Flask-Login uses internally
            yield client

        db.drop_all()

def test_add_comment1(client):
    # Simulate logging in (if your app requires it)
    with client.session_transaction() as sess:
        sess['user'] = {'email': 'test@example.com', 'username': 'testuser'}

    # Post a comment for comment1 field
    response = client.post('/add_comments', data={'comment1': 'This is comment 1'}, follow_redirects=True)
    assert response.status_code == 200

    # Check the comment is added in the database
    comment = Comments.query.filter_by(comment1='This is comment 1').first()
    assert comment is not None

def test_add_comment2(client):
    with client.session_transaction() as sess:
        sess['user'] = {'email': 'test@example.com', 'username': 'testuser'}

    response = client.post('/add_comments', data={'comment2': 'This is comment 2'}, follow_redirects=True)
    assert response.status_code == 200

    comment = Comments.query.filter_by(comment2='This is comment 2').first()
    assert comment is not None

def test_add_no_comment_redirect(client):
    with client.session_transaction() as sess:
        sess['user'] = {'email': 'test@example.com', 'username': 'testuser'}

    response = client.post('/add_comments', data={}, follow_redirects=False)
    # Should redirect to index
    assert response.status_code == 302
    assert response.headers['Location'].endswith(url_for('index'))

def test_delete_comment_as_admin(client):
    # Add a comment to the DB
    comment = Comments(comment1='To be deleted')
    db.session.add(comment)
    db.session.commit()

    # Simulate admin session
    with client.session_transaction() as sess:
        sess['user'] = {'email': 'admin@hw3.com', 'username': 'admin'}
        sess['_user_id'] = 'admin123'
        app_module.users['admin123'] = app_module.User('admin123', 'admin', 'admin@hw3.com')

    # Perform the deletion
    response = client.post(f'/delete/{comment.id}', follow_redirects=True)

    # Check that the comment is gone
    deleted = Comments.query.get(comment.id)
    assert response.status_code == 200
    assert deleted is None

def test_delete_comment_unauthorized(client):
    # Add a comment to the DB
    comment = Comments(comment1='Should not be deleted')
    db.session.add(comment)
    db.session.commit()

    # Simulate normal user session
    with client.session_transaction() as sess:
        sess['user'] = {'email': 'user@hw3.com', 'username': 'user'}
        sess['_user_id'] = 'user123'
        app_module.users['user123'] = app_module.User('user123', 'user', 'user@hw3.com')

    # Attempt to delete
    response = client.post(f'/delete/{comment.id}', follow_redirects=True)

    # Comment should still exist
    still_exists = Comments.query.get(comment.id)
    assert response.status_code == 200
    assert b'Cannot delete comment' in response.data
    assert still_exists is not None
