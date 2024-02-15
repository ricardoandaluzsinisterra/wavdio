from flask import Flask, render_template, request, redirect, url_for, session
import requests
from wavdio_services import validate_user, register_user, check_user
from db_handling import handle_file_upload

app = Flask(__name__)
app.secret_key = 'jese' 

app.config['UPLOAD_FOLDER'] = '/usr/share/nginx/html/audio'

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
        response = requests.get('http://catalog-svc:5004/songs?sort=upload_time&order=desc&limit=10')
        if response.status_code != 200:
            raise Exception(f'Failed to fetch latest uploads: {response.status_code}')
        latest_uploads = response.json()
        return render_template('upload.html.j2', username=session['username'], latest_uploads=latest_uploads)
    except requests.exceptions.RequestException:
        return "catalog-svc is not running. Please start catalog-svc and try again."
    
@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('login')) 

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5002, debug=True)