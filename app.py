from flask import Flask, render_template
import os
from dotenv import load_dotenv
from flask import Flask, render_template
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
nyt_api_key = os.getenv('NYT_API_KEY')


@app.route('/')
def index():
    # Had to compile both sets into one set of stories
    stories = get_stories("Sacramento")
    stories.sort(key=lambda x: x.get("pub_date", ""), reverse=True)
    print(stories)

    return render_template('index.html', stories = stories)

def extract_city_from_keywords(keywords):
    for keyword in keywords:
        if 'sacramento' in keyword.get('value', '').lower():
            return 'Sacramento'
        if 'davis' in keyword.get('value', '').lower():
            return 'Davis'
    return None


def get_stories(location): 
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

    params = {
        'q': 'Davis (Calif) AND Sacramento (Calif))',
        'api-key': nyt_api_key 
    }

    response = requests.get(url, params=params)

    
    if response.status_code == 200:
        data = response.json()
        stories = data.get('response',{}).get('docs')
        for story in stories:
            keywords = story.get('keywords', [])
            city = extract_city_from_keywords(keywords)
            if city:
                story['city'] = city
            else:
                story['city'] = "N/A"
        return stories
    else:
        print("Something went wrong");
        return []



if __name__ == '__main__':
    app.run(debug=True)