from flask import Flask, render_template, request, redirect, url_for, session
from requests.exceptions import RequestException
from wavdio_services import validate_user, register_user, check_user

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
            return redirect(('/home'))
        return render_template('login.html.j2')
    except RequestException:
        return "catalog-svc is not running. Please start catalog-svc and try again."

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
    except RequestException:
        return "catalog-svc is not running. Please start catalog-svc and try again."
    
@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('login')) 

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5001, debug=True)