from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from requests.exceptions import RequestException
from user_authentication import validate_user, register_user, check_user
import os
import logging


logger = logging.getLogger(__name__)


static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, 
           static_folder=static_folder,
           static_url_path='/static')
app.secret_key = 'jese' 

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
)

app.config['UPLOAD_FOLDER'] = './audio/'

@app.route('/')
def root():
    return redirect('/login')

@app.before_request
def log_request():
    logger.debug(f"Incoming request: {request.method} {request.path}")
    logger.debug(f"Static folder path: {app.static_folder}")

@app.errorhandler(404)
def not_found(e):
    logger.error(f"404 error: {request.path}")
    return redirect('/login')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            check_user(username, password)
            session['username'] = username
            return redirect(('/home'))
        return render_template('login.html.j2')
    except Exception as e:
        return render_template('login.html.j2', error=e)

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            validate_user(username, password, confirm_password)
            register_user(username, password)
            return redirect('/login')
        return render_template('register.html.j2')
    except Exception as e:
        return render_template('register.html.j2', error=e)
    
@app.route('/liveness')
def liveness():
    logger.debug("Liveness probe accessed")
    return jsonify(status="alive"), 200

@app.route('/readiness')
def readiness():
    logger.debug("Readiness probe accessed")
    # Add any necessary checks here
    return jsonify(status="ready"), 200

@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect('/login') 

if __name__ == '__main__':
    app.run(ssl_context=('certs/cert.pem', 'certs/key.pem'), host='0.0.0.0', port=443)