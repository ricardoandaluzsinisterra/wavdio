from flask import Flask, render_template, request, redirect, url_for, session
from requests.exceptions import RequestException
from user_authentication import validate_user, register_user, check_user

app = Flask(__name__)
app.secret_key = 'jese' 

app.config['UPLOAD_FOLDER'] = './audio/'

@app.route('/', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            check_user(username, password)
            session['username'] = username
            return redirect(('https://localhost/home'))
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
            return redirect(url_for('login'))
        return render_template('register.html.j2')
    except Exception as e:
        return render_template('register.html.j2', error=e)
    
@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('login')) 

if __name__ == '__main__':
    app.run(ssl_context=('certs/cert.pem', 'certs/key.pem'), host='0.0.0.0', port=443)