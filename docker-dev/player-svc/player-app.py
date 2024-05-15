from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'jese' 

app.config['UPLOAD_FOLDER'] = './audio/'

@app.route('/player/<song_key>')
def player(song_key):
    try:
        if 'username' not in session:
            return redirect('/') 
        response = requests.get(f'http://localhost/catalog/songs/{song_key}')
        if response.status_code != 200:
            raise Exception(f'Failed to fetch song details: {response.status_code}')
        song = response.json()
        return render_template('player.html.j2', username=session['username'], song=song)
    except requests.exceptions.RequestException:
        return "catalog-svc is not running. Please start catalog-svc and try again."
    
@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('login')) 

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)