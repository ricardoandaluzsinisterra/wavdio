from flask import Flask, render_template, request, redirect, url_for, session
#How can I handle the case where Redis is not running?
from redis.exceptions import ConnectionError
from flask_session import Session
import redis
from wavdio_services import validate_user, register_user, check_user
from db_handling import handle_file_upload, fetch_latest_uploads, fetch_all_songs_alphabetically, fetch_song_details

app = Flask(__name__)
app.secret_key = 'jese' 

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='users-db', port=6379, db=0)

sess = Session()
sess.init_app(app)

app.config['UPLOAD_FOLDER'] = './audio/'

@app.route('/home')
def home():
    try:
        if 'username' not in session: 
            return redirect(('/login')) 
        all_songs = fetch_all_songs_alphabetically()  # Fetch all songs in alphabetical order
        return render_template('home.html.j2', username=session['username'], all_songs=all_songs)  
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."

@app.route('/logout')
def logout():
    session.pop('username', None)  
    return redirect('http://user-svc:5000' + url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)