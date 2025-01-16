from flask import Flask, jsonify, request
from kafka import KafkaProducer
import redis
import json
import logging

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.INFO)

songs_db = redis.Redis(host='songs-db', port=6379, db=0)
users_db = redis.Redis(host='users-db', port=6379, db=0)

# Kafka producer configuration
producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

TOPIC_NAME = 'songs'

def send_all_songs_to_kafka():
    logging.info('Sending all songs to Kafka...')
    
    keys = songs_db.keys('song:*')
    
    for key in keys:
        song_data = json.loads(songs_db.get(key).decode('utf-8'))
        
        producer.send(TOPIC_NAME, value=song_data) 
        logging.info(f"Produced song {song_data['title']} to Kafka topic {TOPIC_NAME}")

    producer.flush()

@app.route('/songs', methods=['POST'])
def add_song():
    logging.info('Adding song...')
    song_data = request.get_json()
    if not song_data:
        return jsonify({'message': 'Invalid request'}), 400
    song_id = song_data['id']
    songs_db.set(f'song:{song_id}', json.dumps(song_data))
    producer.send('songs', key=song_id.encode('utf-8'), value=song_data)
    producer.flush()
    logging.info(f"Produced new song {song_id} to Kafka topic 'songs'")

@app.route('/users', methods=['POST'])
def add_user():
    logging.info('add user method called')
    user_data = request.get_json()
    if not user_data:
        return jsonify({'message': 'Invalid request'}), 400
    username = user_data['username']
    users_db.set(f'user:{username}', json.dumps(user_data))
    producer.send('users', key=username.encode('utf-8'), value=user_data)
    producer.flush()
    return jsonify(user_data), 201

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    logging.info(f'get user method called with username {username}')
    user_data = users_db.get(f'user:{username}')
    if not user_data:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(json.loads(user_data.decode('utf-8'))), 200

if __name__ == '__main__':
    send_all_songs_to_kafka()
    app.run(ssl_context=('certs/cert.pem', 'certs/key.pem'), host='0.0.0.0', port=443)