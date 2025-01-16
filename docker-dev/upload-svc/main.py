from flask import Flask, render_template, request, redirect, url_for, session
import requests
import threading
from file_utils import handle_file_upload
import song_consumer

app = Flask(__name__)
app.secret_key = 'jese' 

app.config['UPLOAD_FOLDER'] = '/home/docker/data/songs'

def fetch_songs_periodically():
    thread = threading.Thread(target=song_consumer.consume_songs)
    thread.daemon = True  # This ensures the thread will exit when the main program exits
    thread.start()

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
        # Fetch the latest uploads from catalog-svc
        latest_uploads = sorted(song_consumer.get_songs(), key=lambda song: song.upload_time, reverse=True)
        return render_template('upload.html.j2', username=session['username'], latest_uploads=latest_uploads)
    except requests.exceptions.RequestException as e:
        return f"catalog-svc is not running. Please start catalog-svc and try again. {e}"
    
@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('login')) 

if __name__ == '__main__':
    fetch_songs_periodically()
    app.run(ssl_context=('certs/cert.pem', 'certs/key.pem'), host='0.0.0.0', port=443)