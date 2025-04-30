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
    stories = get_stories()
    stories.sort(key=lambda x: x.get("pub_date", ""), reverse=True)
    limited_stories = stories[:3] 
    print(stories)

    return render_template('index.html', limited_stories = limited_stories, stories = stories)

# We pull directly from articles so the content is relating to Davis and Sac,
# not just the location it was written in
def extract_city_from_keywords(keywords):
    for keyword in keywords:
        if 'sacramento' in keyword.get('value', '').lower():
            return 'Sacramento'
        if 'davis' in keyword.get('value', '').lower():
            return 'Davis'
    return None


def get_stories(): 
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

    params = {
        'q': 'Davis (Calif) AND Sacramento (Calif))',
        'api-key': nyt_api_key 
    }

    response = requests.get(url, params=params)

    
    if response.status_code == 200:
        data = response.json()
        stories = data.get('response',{}).get('docs')

        # Fetch necessary components here for our frontend
        for story in stories:
            story['title'] = story.get('headline', {}).get('main', 'No title')
            story['url'] = story.get('web_url', '#')
            story['summary'] = story.get('abstract', 'No summary')
            keywords = story.get('keywords', [])
            city = extract_city_from_keywords(keywords)
            if city:
                story['city'] = city
            else:
                story['city'] = "N/A"
        return stories
    else:
        print("Something went wrong")
        return []



if __name__ == '__main__':
    app.run(debug=True)