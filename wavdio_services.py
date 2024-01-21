import redis
# How do I encrypt and check passwords on my database?
from werkzeug.security import generate_password_hash, check_password_hash
# How do I handle file uploads?
from werkzeug.utils import secure_filename
import os
from datetime import datetime
# How do I make the database handle the songs information
import uuid


r=redis.Redis(host='localhost', port=6379, db=0)

def validate_user(username, password, confirm_password):
        if password != confirm_password:
            return "Passwords do not match."
        if r.exists(f"user:{username}:password"):
            return "Registration failed. Please try again."
        return None

def register_user(username, password):
    hashed_password = generate_password_hash(password)
    r.set(f"user:{username}:password", hashed_password)
    return None

def check_user(username, password):
    hashed_password = r.get(f"user:{username}:password")
    if hashed_password and check_password_hash(hashed_password.decode('utf-8'), password):
        return None
    else:
        return "Login failed. Please try again."
  
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a'}
    #divides the filename into two parts and checks if the second part is in the set of allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
from datetime import datetime

def handle_file_upload(request, upload_folder):
    if 'file' not in request.files:
        return None, None, None, None, 'No file part in the request'
    file = request.files['file']
    
    if file.filename == '':
        return None, None, None, None, 'No selected file'
    
    if not allowed_file(file.filename):
        return None, None, None, None, 'File type not allowed. Please upload an audio file.'
    
    title = request.form.get('title')
    author = request.form.get('author')
    album = request.form.get('album')
    filename = secure_filename(file.filename)
    if r.exists(f"song:{title}"):
        return None, None, None, None, 'A song with the same title already exists.'
    
    filename = secure_filename(file.filename)
    if os.path.exists(os.path.join(upload_folder, filename)):
        return None, None, None, None, 'A file with the same name already exists.'
    
    file.save(os.path.join(upload_folder, filename))
    song_id = f"song:{str(uuid.uuid4())}"
    r.hset(song_id, mapping={
        'filename': filename,
        'title': title,
        'author': author,
        'album': album,
        'upload_time': datetime.now().isoformat()
    })
    
    return filename, title, author, album, None

def fetch_latest_uploads():
    keys = r.keys()
    latest_uploads = []
    
    for key in keys:
        key = key.decode('utf-8')  # Decode key to string
        key_type = r.type(key).decode('utf-8')  # Decode type to string
        if key_type == 'hash':
            song_info = r.hgetall(key)
            # Decode bytes to strings
            song_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in song_info.items()}
            if 'upload_time' in song_info:
                latest_uploads.append(song_info)
            
    
    latest_uploads.sort(key=lambda song: song['upload_time'], reverse=True)
    
    return latest_uploads[:10]

def fetch_all_songs_alphabetically():
    keys = r.keys()
    all_songs = []
    
    for key in keys:
        key = key.decode('utf-8') 
        key_type = r.type(key).decode('utf-8') 
        if key_type == 'hash':
            song_info = r.hgetall(key)
            song_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in song_info.items()}
            song_info['key'] = key 
            if 'title' in song_info:
                all_songs.append(song_info)
            
    all_songs.sort(key=lambda song: song['title'])
    
    return all_songs

#How can I decode the song for playback
def fetch_song_details(song_key):
    song_info = r.hgetall(song_key)
    song_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in song_info.items()}
    return song_info