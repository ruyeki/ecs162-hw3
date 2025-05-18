from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
import json
import requests
import jsonify
from flask_login import LoginManager, login_required
from flask_login import login_user
from flask_login import UserMixin

login_manager = LoginManager()
login_manager.login_view = 'login'  # The name of your login route function

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app.secret_key = 'Test'  # Use a long random string in production


nyt_api_key = os.getenv('NYT_API_KEY')

login_manager.init_app(app)


#hardcoded the username and password for now
class User(UserMixin):
    def __init__(self):
        self.id = 1
        self.username = "demo"
        self.password = "test"

@login_manager.user_loader
def load_user(user_id):
    # Return the same dummy user if the ID matches
    if user_id == "1":
        return user
    return None

user = User()



@app.route('/')
@login_required
def index():
    stories = get_stories()
    stories.sort(key=lambda x: x.get("pub_date", ""), reverse=True)
    limited_stories = stories[:3] 
    #print("These are the stories:", stories)

    return render_template('index.html', limited_stories=limited_stories, stories=stories)

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
        #print(json.dumps(data, indent=2))
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



@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST": 
        username = request.form['username']
        password = request.form['password']

        if username == user.username and password == user.password: 
            login_user(user)
            return redirect(url_for('index'))
        else: 
            return "Failed to login"
    

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)