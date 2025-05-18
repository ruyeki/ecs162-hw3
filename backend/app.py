from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv
import json
import requests
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin
from authlib.integrations.flask_client import OAuth

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'a_very_secret_key_for_dev_1234567890'


nyt_api_key = os.getenv('NYT_API_KEY')

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Authlib OIDC (Dex) setup
oauth = OAuth(app)

oauth.register(
    name='dex',
    client_id=os.getenv('DEX_CLIENT_ID', 'flask-app'),
    client_secret=os.getenv('DEX_CLIENT_SECRET', 'flask-secret'),
    server_metadata_url=os.getenv('DEX_METADATA_URL', 'http://localhost:5556/.well-known/openid-configuration'),
    client_kwargs={'scope': 'openid email profile'},
)

# Dummy user class and user storage
class User(UserMixin):
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

users = {}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
@login_required
def index():
    stories = get_stories()
    stories.sort(key=lambda x: x.get("pub_date", ""), reverse=True)
    limited_stories = stories[:3]
    return render_template('index.html', limited_stories=limited_stories, stories=stories)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.dex.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.dex.authorize_access_token()
    nonce = session.get('oauth_nonce')
    userinfo = oauth.dex.parse_id_token(token, nonce)
    user = User(userinfo['sub'], userinfo.get('name', 'Unknown'), userinfo.get('email', 'unknown@example.com'))
    users[user.id] = user
    login_user(user)
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

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
        'q': 'Davis (Calif) AND Sacramento (Calif)',
        'api-key': nyt_api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        stories = data.get('response', {}).get('docs', [])
        for story in stories:
            story['title'] = story.get('headline', {}).get('main', 'No title')
            story['url'] = story.get('web_url', '#')
            story['summary'] = story.get('abstract', 'No summary')
            keywords = story.get('keywords', [])
            city = extract_city_from_keywords(keywords)
            story['city'] = city if city else "N/A"
        return stories
    else:
        print("Error fetching stories")
        return []

if __name__ == '__main__':
    app.run(debug=True, port=8000)
