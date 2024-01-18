from flask import Flask, render_template, request, redirect, url_for
from database import register_user

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Here you can check the username and password
        # If they are valid, you can redirect the user to the main page
        return redirect(url_for('home'))
    return render_template('login.html.j2')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            error = "Passwords do not match."
            return render_template('register.html.j2', error=error)
        error = register_user(username, password)
        if error:
            return render_template('register.html.j2', error=error)
        return redirect(url_for('index'))
    return render_template('register.html.j2')

@app.route('/home')
def home():
    # The main page of your app
    return render_template('home.html.j2')

if __name__ == '__main__':
    app.run(debug=True)