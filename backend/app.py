from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from dotenv import load_dotenv
import json
import requests
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin
from authlib.integrations.flask_client import OAuth
import sqlite3
from models import db, Comments

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'a_very_secret_key_for_dev_1234567890'

#setting up the sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    #db.drop_all()
    db.create_all()


nyt_api_key = os.getenv('NYT_API_KEY')

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# setting up dex
oauth = OAuth(app)
oauth.register(
    name='dex',
    client_id=os.getenv('DEX_CLIENT_ID', 'flask-app'),
    client_secret=os.getenv('DEX_CLIENT_SECRET', 'flask-secret'),
    server_metadata_url=os.getenv('DEX_METADATA_URL', 'http://localhost:5556/.well-known/openid-configuration'),
    client_kwargs={'scope': 'openid email profile'},
    redirect_uri='http://localhost:8000/authorize'
)


users = {}
class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

#API end point for adding comments to a certain article
@app.route('/add_comments', methods = ['POST'])
def add_comments(): 

    comment_text1 = request.form.get('comment1')
    comment_text2 = request.form.get('comment2')
    comment_text3 = request.form.get('comment3')

    if comment_text1:
        new_comment = Comments(comment1=comment_text1)
    elif comment_text2:
        new_comment = Comments(comment2=comment_text2)
    elif comment_text3:
        new_comment = Comments(comment3=comment_text3)
    else:
        # No comment submitted, handle error or redirect
        return redirect(url_for('index'))

    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    comments = Comments.query.all()
    stories = get_stories()
    stories.sort(key=lambda x: x.get("pub_date", ""), reverse=True)
    limited_stories = stories[:3]
    userinfo = session.get('user')
    user_email = userinfo.get('email')
    return render_template('index.html', user_email = user_email, comments = comments, limited_stories=limited_stories, stories=stories)


#API endpoint for deleting a certain comment based on its id
@app.route('/delete/<int:id>', methods = ['POST'])
def delete(id): 

    userinfo = session.get('user')
    print(userinfo)

    allowed_users = ["admin@hw3.com", "moderator@hw3.com"]

    if userinfo.get('email') not in allowed_users:
        return "Cannot delete comment. Not an admin or moderator."
    comment_to_delete = Comments.query.get_or_404(id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


#route for logging in a user
@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.dex.authorize_redirect(redirect_uri)

#route for authoirizing a user login
@app.route('/authorize')
def authorize():
    token = oauth.dex.authorize_access_token()
    nonce = session.get('oauth_nonce')
    userinfo = oauth.dex.parse_id_token(token, nonce)
    user = User(userinfo['sub'], userinfo.get('username', 'Unknown'), userinfo.get('email', 'unknown@example.com'))
    users[user.id] = user
    session['user'] = {
        'username': userinfo.get('username'),
        'email': userinfo.get('email'),
    }
    login_user(user)
    return redirect(url_for('index'))

#route for logging out a user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

def extract_city_from_keywords(keywords):
    for keyword in keywords:
        if 'sacramento' in keyword.get('value', '').lower():
            return 'Sacramento'
        if 'davis' in keyword.get('value', '').lower():
            return 'Davis'
    return None

#API endpoint for getting a story from nyt api
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
