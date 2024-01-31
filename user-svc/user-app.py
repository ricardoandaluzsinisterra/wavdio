from flask import Flask, render_template, request, redirect, url_for, session
#How can I handle the case where Redis is not running?
from redis.exceptions import ConnectionError
from wavdio_services import validate_user, register_user, check_user
from db_handling import handle_file_upload, fetch_latest_uploads, fetch_all_songs_alphabetically, fetch_song_details

app = Flask(__name__)
app.secret_key = 'jese' 

app.config['UPLOAD_FOLDER'] = './audio/'

@app.route('/', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            error = check_user(username, password)
            if error:
                return render_template('login.html.j2', error=error)
            session['username'] = username  
            return redirect(url_for('home'))
        return render_template('login.html.j2')
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            error = validate_user(username, password, confirm_password)
            if error:
                return render_template('register.html.j2', error=error)
            register_user(username, password)
            return redirect(url_for('login'))
        return render_template('register.html.j2')
    except ConnectionError:
        return "Redis is not running. Please start Redis and try again."

if __name__ == '__main__':
    app.run(debug=True)