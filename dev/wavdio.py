from flask import Flask, render_template, request, redirect, url_for, session
#How can I handle the case where Redis is not running?
from redis.exceptions import ConnectionError
from wavdio_services import validate_user, register_user, check_user, handle_file_upload, fetch_latest_uploads, fetch_all_songs_alphabetically, fetch_song_details

app = Flask(__name__)
app.secret_key = 'jese' 

app.config['UPLOAD_FOLDER'] = './audio/'

@app.route('/', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            error = check_user(username, password)
            if error:
                return render_template('login.html.j2', error=error)
            session['username'] = username  
            return redirect(url_for('home'))
        return render_template('login.html.j2')
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            error = validate_user(username, password, confirm_password)
            if error:
                return render_template('register.html.j2', error=error)
            register_user(username, password)
            return redirect(url_for('login'))
        return render_template('register.html.j2')
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."

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

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        if 'username' not in session:
            return redirect(url_for('login')) 
        if request.method == 'POST':
            filename, title, author, album, error = handle_file_upload(request, app.config['UPLOAD_FOLDER'])
            if error:
                return render_template('upload.html.j2', username=session['username'], error=error)
            if filename:
                success_message = f"Uploaded {title} by {author} from the album {album}."
                return render_template('upload.html.j2', username=session['username'], success=success_message)
        # Fetch the latest uploads from Redis
        latest_uploads = fetch_latest_uploads()
        return render_template('upload.html.j2', username=session['username'], latest_uploads=latest_uploads)
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."

@app.route('/history')
def history():
    try:
        if 'username' not in session:
            return redirect(url_for('login')) 
        return render_template('history.html.j2', username=session['username'])
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."

@app.route('/player/<song_key>')
def player(song_key):
    try:
        if 'username' not in session:
            return redirect(url_for('login')) 
        song = fetch_song_details(song_key)
        return render_template('player.html.j2', username=session['username'], song=song)
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."

if __name__ == '__main__':
    app.run(debug=True)