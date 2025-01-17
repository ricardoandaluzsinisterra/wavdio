from flask import Flask, render_template, request, redirect, url_for, session
import song_consumer
import logging
import threading
import os

static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, 
           static_folder=static_folder,
           static_url_path='/static')
app.secret_key = 'jese'

def fetch_songs_periodically():
    logger = logging.getLogger(__name__)
    logger.info("Starting Kafka consumer thread...")
    thread = threading.Thread(target=song_consumer.consume_songs)
    thread.daemon = True
    thread.start()
    logger.info("Kafka consumer thread started")

app.config['AUDIO_PATH'] = '/usr/share/nginx/html/audio'

@app.route('/player/<song_title>')
def player(song_title):
    try:
        if 'username' not in session:
            return redirect(url_for('login'))
            
        logging.debug(f"Looking up song: {song_title}")
        song = song_consumer.get_song(song_title)
        
        if not song:
            logging.error(f"Song not found in cache: {song_title}")
            raise Exception(f'Song not found: {song_title}')
        
        logging.debug(f"Found song data: {song}")
        
        filename = f"{song_title}.mp3"
        audio_path = os.path.join(app.config['AUDIO_PATH'], filename)
        
        # Debug filesystem
        logging.debug(f"Checking directory contents:")
        try:
            files = os.listdir(app.config['AUDIO_PATH'])
            logging.debug(f"Files in {app.config['AUDIO_PATH']}: {files}")
        except Exception as e:
            logging.error(f"Error listing directory: {e}")
            
        logging.debug(f"Checking file: {audio_path}")
        logging.debug(f"File exists: {os.path.exists(audio_path)}")
        
        if not os.path.exists(audio_path):
            logging.error(f"Audio file not found: {audio_path}")
            return render_template('error.html.j2', 
                                error=f"Audio file not found: {filename}",
                                username=session['username'])
                                
        # Simplified song dict
        song_dict = {
            'title': song.get('title', song_title),
            'author': song.get('author', 'Unknown'),
            'album': song.get('album', 'Unknown'),
            'filename': filename
        }
            
        return render_template('player.html.j2',
                             username=session['username'],
                             song=song_dict)
                             
    except Exception as e:
        logging.error(f"Player error: {str(e)}")
        return render_template('error.html.j2',
                             error=f"Error playing song: {str(e)}",
                             username=session.get('username'))
    
@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('login')) 

if __name__ == '__main__':
    fetch_songs_periodically()
    app.run(ssl_context=('certs/cert.pem', 'certs/key.pem'), host='0.0.0.0', port=443)