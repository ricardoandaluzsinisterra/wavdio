import redis
# How do I encrypt and check passwords on my database?
from werkzeug.security import generate_password_hash, check_password_hash
# How do I handle file uploads?
from werkzeug.utils import secure_filename
import os
from datetime import datetime
# How do I make the database handle the songs information
import uuid

def allowed_file(filename):
    extensions = {'mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a'}
    #divides the filename into two parts and checks if the second part is in the set of allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

import requests
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

def handle_file_upload(request, upload_folder):
    # Check if the post request has the file part
    if 'file' not in request.files:
        return None, None, None, None, 'No file part in the request.'

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return None, None, None, None, 'No selected file.'

    if file and allowed_file(file.filename):
        title = request.form.get('title')
        author = request.form.get('author')
        album = request.form.get('album')
        filename = secure_filename(file.filename)

        # Check if a song with the same title already exists
        response = requests.get(f'http://catalog-svc:5004/songs?title={title}')
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
        response = requests.post('http://catalog-svc:5004/songs', json=song_data)
        if response.status_code != 201:
            raise Exception(f'Failed to add song: {response.status_code}')

        return filename, title, author, album, None

    return None, None, None, None, 'Allowed file types are txt, pdf, png, jpg, jpeg, gif.'