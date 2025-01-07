from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)

# App configuration
app.secret_key = os.getenv('SECRET_KEY')  # Secret key from .env
app.config['SESSION_PERMANENT'] = True  # Enable permanent session
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
    minutes=30)  # Session timeout: 30 minutes

# Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),  # Google Client ID from .env
    # Google Client Secret from .env
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account'  # Forces Google to show the account selector
    }
)

# Routes


@app.route('/')
def index():
    email = session.get('email')
    name = session.get('name')
    picture = session.get('picture')
    return render_template('index.html', email=email, name=name, picture=picture)


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        if user_info:
            session.clear()  # Clear session before storing new user data
            session['email'] = user_info['email']
            session['name'] = user_info['name']
            session['picture'] = user_info['picture']
        return redirect('/')
    except Exception as e:
        return f"An error occurred during authorization: {e}", 500


@app.route('/logout')
def logout():
    # Clear the session in the Flask app
    session.clear()

    # Force Google account logout and redirect back to the home page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
