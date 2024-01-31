from flask import Flask, render_template, request, redirect, url_for, session
#How can I handle the case where Redis is not running?
from redis.exceptions import ConnectionError
from wavdio_services import validate_user, register_user, check_user, handle_file_upload, fetch_latest_uploads, fetch_all_songs_alphabetically, fetch_song_details

app = Flask(__name__)
app.secret_key = 'jese' 

app.config['UPLOAD_FOLDER'] = './audio/'

@app.route('/home')
def home():
    try:
        if 'username' not in session:
            return redirect(url_for('login')) 
        all_songs = fetch_all_songs_alphabetically()  # Fetch all songs in alphabetical order
        return render_template('home.html.j2', username=session['username'], all_songs=all_songs)
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."

@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('login')) 

if __name__ == '__main__':
    app.run(debug=True)