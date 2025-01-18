# How do I encrypt and check passwords on my database?
from werkzeug.security import generate_password_hash, check_password_hash
# How do I handle file uploads?
from werkzeug.utils import secure_filename
import os
from datetime import datetime
# How do I make the database handle the songs information
import uuid
import requests
import song_consumer
from exceptions import *
from Song import Song

songs  = []
CATALOG_URL = os.getenv('CATALOG_URL', '/catalog')


def song_exists(song):
    global songs
    for current_song in songs:
        if current_song == song:
            raise SongError("There is already a copy on this song in the system")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'mp3'

def handle_file_upload(request, upload_folder):
    global songs

    # Check if a file was uploaded
    if 'file' not in request.files:
        raise FileNotFoundError("No file in request")

    file = request.files['file']

    if not allowed_file(file.filename):
        raise TypeError("Allowed file type is mp3")
    
    if file.filename == '':
        raise FileNotFoundError("No file selected")

    if file and allowed_file(file.filename):
        title = request.form.get('title')
        author = request.form.get('author')
        album = request.form.get('album')

        song = Song(title=title, author=author, album=album)
        song_exists(song)

        #
        filename = f"{title}.mp3"
        file.save(os.path.join(upload_folder, filename))
        
        response = requests.post(f'{CATALOG_URL}/songs', verify=False, json=song.to_dict())
        if response.status_code != 201:
            raise SongError(f'Failed to add song: {response.status_code}, {response.text}')

        songs.append(song)

