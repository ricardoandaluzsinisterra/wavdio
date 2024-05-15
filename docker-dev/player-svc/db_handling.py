# How do I encrypt and check passwords on my database?
from werkzeug.security import generate_password_hash, check_password_hash
# How do I handle file uploads?
from werkzeug.utils import secure_filename
import os
from datetime import datetime
# How do I make the database handle the songs information
import uuid
import requests

def allowed_file(filename):
    extensions = {'mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a'}
    # Divides the filename into two parts and checks if the second part is in the set of allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def handle_file_upload(request, upload_folder):
    # Check if the a file was uploaded before processing it
    if 'file' not in request.files:
        return None, None, None, None, 'No file part in the request.'

    file = request.files['file']

    if file.filename == '':
        return None, None, None, None, 'No selected file.'

    if file and allowed_file(file.filename):
        title = request.form.get('title')
        author = request.form.get('author')
        album = request.form.get('album')
        filename = secure_filename(file.filename)

        # Check if a song with the same title already exists
        response = requests.get(f'http://localhost/catalog/songs?title={title}')
        if response.status_code == 200 and response.json():
            return None, None, None, None, 'A song with the same title already exists.'

        file.save(os.path.join(upload_folder, filename))

        song_id = f"song:{str(uuid.uuid4())}"
        song_data = {
            'id': song_id,
            'filename': filename,
            'title': title,
            'author': author,
            'album': album,
            'upload_time': datetime.now().isoformat()
        }
        response = requests.post('http://localhost/catalog/songs', json=song_data)
        if response.status_code != 201:
            raise Exception(f'Failed to add song: {response.status_code}')

        return filename, title, author, album, None

    return None, None, None, None, 'Allowed file types are txt, pdf, png, jpg, jpeg, gif.'