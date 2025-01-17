from flask import Flask, render_template, request, redirect, url_for, session
import song_consumer
import threading
import logging
import os


static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, 
           static_folder=static_folder,
           static_url_path='/static')
app.secret_key = 'jese'

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
)

logger = logging.getLogger(__name__)

@app.before_request
def debug_session():
    logger.debug(f"Session username: {session.get('username', 'Not logged in')}")
    logger.debug(f"Cookies: {request.cookies}")


app.config['UPLOAD_FOLDER'] = './audio/'

def fetch_songs_periodically():
    logger = logging.getLogger(__name__)
    logger.info("Starting Kafka consumer thread...")
    thread = threading.Thread(target=song_consumer.consume_songs)
    thread.daemon = True
    thread.start()
    logger.info("Kafka consumer thread started")

@app.route('/')
@app.route('/home')
def home():
    try:
        if 'username' not in session:
            return redirect('/user/login')
        songs = song_consumer.get_songs()
        logging.info(f"Retrieved {len(songs)} songs from consumer")
        upload_url = os.getenv('UPLOAD_URL', '/upload')
        return render_template('home.html.j2', username=session['username'], all_songs=songs, upload_url=upload_url)
    except Exception as e:
        return f"An error occurred: {str(e)}"


#Why was there an upload method here?


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/user/login')

if __name__ == '__main__':
    fetch_songs_periodically()
    app.run(ssl_context=('certs/cert.pem', 'certs/key.pem'), host='0.0.0.0', port=443)