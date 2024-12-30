from flask import Flask, render_template, request, redirect, url_for, session
from kafka import KafkaConsumer
import threading
import json

app = Flask(__name__)
app.secret_key = 'jese'

app.config['UPLOAD_FOLDER'] = './audio/'

# Local data structures to store songs and users
songs_data = {}
users_data = {}

# Kafka consumer configuration for songs
songs_consumer = KafkaConsumer(
    'songs',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='home-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Kafka consumer configuration for users
users_consumer = KafkaConsumer(
    'users',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='home-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

def consume_songs():
    for msg in songs_consumer:
        key = msg.key.decode('utf-8')
        value = msg.value
        songs_data[key] = value

def consume_users():
    for msg in users_consumer:
        key = msg.key.decode('utf-8')
        value = msg.value
        users_data[key] = value

# Start Kafka consumers in separate threads
songs_consumer_thread = threading.Thread(target=consume_songs)
songs_consumer_thread.start()

users_consumer_thread = threading.Thread(target=consume_users)
users_consumer_thread.start()

@app.route('/home')
def home():
    print('in home')
    try:
        if 'username' not in session:
            return redirect('/')
        all_songs = list(songs_data.values())
        return render_template('home.html.j2', username=session['username'], all_songs=all_songs)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/users')
def users():
    print('in users')
    try:
        if 'username' not in session:
            return redirect('/')
        all_users = list(users_data.values())
        return render_template('users.html.j2', username=session['username'], all_users=all_users)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)