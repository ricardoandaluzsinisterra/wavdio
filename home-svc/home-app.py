from flask import Flask, render_template, request, redirect, url_for, session
import requests
from wavdio_services import validate_user, register_user, check_user

app = Flask(__name__)
app.secret_key = 'jese' 

app.config['UPLOAD_FOLDER'] = './audio/'

@app.route('/home')
def home():
    try:
        if 'username' not in session:
            return redirect('/') 
        response = requests.get('http://catalog-svc:5004/songs?sort=title&order=asc')
        if response.status_code != 200:
            raise Exception(f'Failed to fetch all songs: {response.status_code}')
        all_songs = response.json()
        return render_template('home.html.j2', username=session['username'], all_songs=all_songs)
    except requests.exceptions.RequestException:
        return "catalog-svc is not running. Please start catalog-svc and try again."

@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('login'))  

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)