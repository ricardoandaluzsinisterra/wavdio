from flask import Flask, jsonify, request
from kafka import KafkaProducer
import redis
import json
import logging
from Song import Song
import os

app = Flask(__name__)

SONGS_REDIS_HOST = os.getenv("SONGS_REDIS_HOST")
USERS_REDIS_HOST = os.getenv("USERS_REDIS_HOST")

logging.basicConfig(filename='app.log', level=logging.INFO)

songs_db = redis.Redis(host=SONGS_REDIS_HOST, port=6379, db=0)
users_db = redis.Redis(host=USERS_REDIS_HOST, port=6379, db=0)

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")

# Kafka producer configuration
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

TOPIC_NAME = 'songs'

def on_send_success(record_metadata):
    logging.info(f"Message successfully sent to {record_metadata.topic} with offset {record_metadata.offset}")
    
def on_send_error(excp):
    logging.error(f"Error sending message: {excp}")

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
        return jsonify({'message': 'Invalid request, no data provided.'}), 400

    try:
        # Deserialize the incoming JSON into a Song object
        song = Song.from_dictionary(song_data)
        
        songs_db.set(f'song:{song.title}', json.dumps(song.to_dict()))
        logging.info(f"Set song in DB: {song.title}")
        logging.info(f"Song in DB after set: {songs_db.get(f'song:{song.title}')}")

        producer.send('songs', key=str(song.title).encode('utf-8'), value=song.to_dict()).add_callback(on_send_success).add_errback(on_send_error)
        producer.flush()

        logging.info(f"Produced new song {song.title} to Kafka topic 'songs'")
        song_key = f'song:{song.title}'
        logging.info(f"Attempting to retrieve song with key: {song_key}")
        song_data = songs_db.get(song_key)
        logging.info(f"Song data retrieved: {song_data}")
        logging.info(f"Current songs in DB: {songs_db.keys()}")
        return jsonify(song.to_dict()), 201

    except Exception as e:
        logging.error(f"Error adding song: {str(e)}")
        return jsonify({'message': f'Failed to add song: {str(e)}'}), 500

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