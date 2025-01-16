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

def song_exists(song):
    global songs
    for current_song in songs:
        if current_song == song:
            raise SongError("There is already a copy on this song in the system")

def allowed_file(filename):
    extensions = {'mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a'}
    # Divides the filename into two parts and checks if the second part is in the set of allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def handle_file_upload(request, upload_folder):
    global songs

    # Check if a file was uploaded
    if 'file' not in request.files:
        raise FileNotFoundError("No file in request")

    file = request.files['file']

    if file.filename == '':
        raise FileNotFoundError("No file selected")

    if file and allowed_file(file.filename):
        title = request.form.get('title')
        author = request.form.get('author')
        album = request.form.get('album')

        song = Song(title=title, artist=author, album=album)
        song_exists(song)

        # Save the file
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))

        response = requests.post('https://catalog/songs', json=song.to_dict())
        if response.status_code != 201:
            raise SongError(f'Failed to add song: {response.status_code}, {response.text}')

        songs.append(song)

        return filename, title, author, album, None

    raise TypeError('Allowed file types are mp3, wav, flac, aac, ogg, m4a.')
