from flask import Flask, render_template, request, redirect, url_for, session
from file_utils import handle_file_upload
import song_consumer

app = Flask(__name__)
app.secret_key = 'jese'

app.config['UPLOAD_FOLDER'] = './audio/'


def fetch_songs_periodically():
    thread = threading.Thread(target=song_consumer.consume_songs)
    thread.daemon = True  # This ensures the thread will exit when the main program exits
    thread.start()

@app.route('/home')
def home():
    try:
        if 'username' not in session:
            return redirect('/')
        songs = song_consumer.get_songs()
        return render_template('home.html.j2', username=session['username'], all_songs=songs)
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        filename, title, author, album, error = handle_file_upload(request, app.config['UPLOAD_FOLDER'])
        if error:
            return f"An error occurred: {error}"
        return redirect(url_for('home'))
    return render_template('upload.html.j2')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(ssl_context=('certs/cert.pem', 'certs/key.pem'), host='0.0.0.0', port=443)