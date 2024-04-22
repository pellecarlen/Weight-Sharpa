import os
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Necessary to keep user sessions
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_fallback_secret_key')

# Routes for login and logout
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    # This should clear the session handled by Firebase Authentication
    return redirect(url_for('login'))

@app.route('/register')
def register():
    # Registration can be handled directly by Firebase Authentication on the client-side
    return render_template('register.html')

# Home page that requires login
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Configuring the server to listen on all public addresses on port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
