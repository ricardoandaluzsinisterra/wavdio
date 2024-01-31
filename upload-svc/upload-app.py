from flask import Flask, render_template, request, redirect, url_for
#How can I handle the case where Redis is not running?
from redis.exceptions import ConnectionError
import redis
from flask_session import Session
from wavdio_services import validate_user, register_user, check_user
from db_handling import handle_file_upload, fetch_latest_uploads, fetch_all_songs_alphabetically, fetch_song_details

app = Flask(__name__)
app.secret_key = 'jese' 

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='users-db', port=6379, db=0)

Session(app) 

app.config['UPLOAD_FOLDER'] = 'app/audio/'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        if 'username' not in Session:
            return redirect(('/login')) 
        if request.method == 'POST':
            filename, title, author, album, error = handle_file_upload(request, app.config['UPLOAD_FOLDER'])
            if error:
                return render_template('upload.html.j2', username=Session['username'], error=error)
            if filename:
                success_message = f"Uploaded {title} by {author} from the album {album}."
                return render_template('upload.html.j2', username=Session['username'], success=success_message)
        # Fetch the latest uploads from Redis
        latest_uploads = fetch_latest_uploads()
        return render_template('upload.html.j2', username=Session['username'], latest_uploads=latest_uploads)
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."
    
@app.route('/logout')
def logout():
    Session.pop('username', None) 
    return redirect(('/user')) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False, use_reloader=False)