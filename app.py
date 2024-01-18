from flask import Flask, render_template, request, redirect, url_for
from database import register_user

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Here you can check the username and password
        # If they are valid, you can redirect the user to the main page
        return redirect(url_for('main_page'))
    return render_template('login.html.j2')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        register_user(username, password)
    # Redirect to the registration form page
    return render_template('register.html.j2')

@app.route('/home')
def main_page():
    # The main page of your app
    return render_template('index.html.j2')