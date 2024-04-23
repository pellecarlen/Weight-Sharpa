import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from google.cloud import secretmanager
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Flask app
app = Flask(__name__)

# Function to retrieve secrets from Google Cloud Secret Manager
def get_secret(secret_name):
    """Retrieve a secret value from Google Cloud Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')

# Use secret to set Flask secret key
app.secret_key = get_secret('FLASK_SECRET_KEY')

# Initialize Firebase Admin SDK with Application Default Credentials
firebase_admin.initialize_app(credentials.ApplicationDefault())
db = firestore.client()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        api_key = get_secret('FIREBASE_API_KEY')  # Retrieve API key from Secret Manager

        # Firebase REST API endpoint for verifying user password
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        response = requests.post(url, json=data, headers=headers)
        user_info = response.json()

        print("API Response:", user_info)  # Log the response from Firebase

        if response.status_code == 200:
            if not user_info.get('emailVerified', False):  # Safe check for email verification
                flash('Please verify your email address.')
                return redirect(url_for('login'))
            session['user_id'] = user_info['localId']
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials or user not found.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['firstname']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

        try:
            user_record = auth.create_user(
                email=email,
                password=password,
                display_name=firstname
            )
            auth.send_email_verification(user_record.uid)

            # Store additional user information in Firestore
            user_data = {
                'uid': user_record.uid,
                'firstname': firstname,
                'email_verified': False
            }
            db.collection('userData').document(user_record.uid).set(user_data)

            flash('Registration successful. Please check your email to verify your account.')
            return redirect(url_for('login'))
        except firebase_admin.exceptions.FirebaseError as e:
            flash(f'Error registering user: {str(e)}')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def home():
    user_id = session.get('user_id')
    if user_id:
        user = auth.get_user(user_id)
        return render_template('index.html', user=user)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
