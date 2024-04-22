from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager

app = Flask(__name__)

# Necessary to keep user sessions
app.secret_key = 'your_secret_key_here'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# A simple user class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Temporary user database
users = {'admin': {'password': 'admin'}}

# User Loader
@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        return None
    user = User(user_id)
    return user

# Routes for login and logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Home page that requires login
@app.route('/')
@login_required
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Configuring the server to listen on all public addresses on port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
