from flask import Flask, render_template, request, redirect, url_for
from wavdio_services import validate_user, register_user, check_user

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = check_user(username, password)
        if error:
            return render_template('login.html.j2', error=error)
        return redirect(url_for('home'))
    return render_template('login.html.j2')

@app.route('/register', methods=['GET', 'POST'])
def register():
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

@app.route('/home')
def home():
    # The main page of your app
    return render_template('home.html.j2')

if __name__ == '__main__':
    app.run(debug=True)