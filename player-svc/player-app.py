from flask import Flask, render_template, request, redirect, url_for
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

Session(app) 

app.config['UPLOAD_FOLDER'] = './audio/'


@app.route('/player/<song_key>')
def player(song_key):
    try:
        if 'username' not in Session:
            return redirect(('/login')) 
        song = fetch_song_details(song_key)
        return render_template('player.html.j2', username=Session['username'], song=song)
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."

@app.route('/logout')
def logout():
    Session.pop('username', None) 
    return redirect(('/user')) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False, use_reloader=False)