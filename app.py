from flask import Flask, render_template
import os
from dotenv import load_dotenv
from flask import Flask, render_template
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
NYT_API_KEY = os.getenv("NYT_API_KEY")

nyt_api_key = os.getenv('NYT_API_KEY')


@app.route('/')
def index():

    stories = get_stories()

    print(stories)


    return render_template('index.html', stories = stories)


def get_stories(): 
    url = 'https://api.nytimes.com/svc/topstories/v2/home.json'
    params = {'api-key': nyt_api_key}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()['results']
    else:
        return []



if __name__ == '__main__':
    app.run(debug=True)