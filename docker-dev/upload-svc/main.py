from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import threading
from file_utils import handle_file_upload
import song_consumer
import logging
import os


logger = logging.getLogger(__name__)

static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, 
           static_folder=static_folder,
           static_url_path='/static')
app.secret_key = 'jese'

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
)

app.config['UPLOAD_FOLDER'] = '/usr/share/nginx/html/audio'

@app.before_request
def debug_session():
    logger.debug(f"Session username: {session.get('username', 'Not logged in')}")
    logger.debug(f"Cookies: {request.cookies}")


def fetch_songs_periodically():
    logger = logging.getLogger(__name__)
    logger.info("Starting Kafka consumer thread...")
    thread = threading.Thread(target=song_consumer.consume_songs)
    thread.daemon = True
    thread.start()
    logger.info("Kafka consumer thread started")

@app.route('/')
@app.route('/form', methods=['GET', 'POST'])
def upload():
    try:
        logger.info('username')
        if 'username' not in session:
            logger.info("redirecting to login")
            logger.info('username')
            return redirect('/user/login')

        if request.method == 'POST':
            handle_file_upload(request, app.config['UPLOAD_FOLDER'])
            title = request.form.get('title')
            author = request.form.get('author')
            album = request.form.get('album')
            success_message = f"Uploaded {title} by {author} from the album {album}."
            logging.info(success_message)
            return render_template('upload.html.j2', username=session['username'], success=success_message)

        songs = song_consumer.get_songs()
        logging.info(f"Retrieved {len(songs)} songs from consumer")
        latest_uploads = sorted(songs, key=lambda s: s.upload_time, reverse=True)
        logging.info(f"Latest uploads: {latest_uploads}")

        return render_template('upload.html.j2', 
                            username=session['username'], 
                            latest_uploads=latest_uploads)

    except Exception as e:
        logging.error(f"Error during upload: {str(e)}")
        return render_template('upload.html.j2', username=session['username'],error=str(e))

@app.route('/liveness')
def liveness():
    logger.debug("Liveness probe accessed")
    return jsonify(status="alive"), 200

@app.route('/readiness')
def readiness():
    logger.debug("Readiness probe accessed")
    # Add any necessary checks here
    return jsonify(status="ready"), 200

@app.route('/logout')
def logout():
    session.pop('username', None)
    
    return redirect('/user/login')

if __name__ == '__main__':
    # Start the song consumer in the background when the app runs
    fetch_songs_periodically()
    app.run(ssl_context=('certs/cert.pem', 'certs/key.pem'), host='0.0.0.0', port=443)