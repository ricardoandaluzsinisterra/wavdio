from flask import Flask, render_template, request, redirect, url_for, session
import song_consumer
import threading


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


#Why was there an upload method here?


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    fetch_songs_periodically()
    app.run(ssl_context=('certs/cert.pem', 'certs/key.pem'), host='0.0.0.0', port=443)