from flask import Flask, jsonify, request, Response
from kafka import KafkaProducer
import json
import logging
from Song import Song
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os
from redis.sentinel import Sentinel
import sys

app = Flask(__name__)

SONG_REQUESTS = Counter('song_requests_total', 'Total song requests')
USER_REQUESTS = Counter('user_requests_total', 'Total user requests')
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")


sys.stdout.reconfigure(line_buffering=True)

# Update logger config
logger = logging.getLogger('catalog-service')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Starting Catalog Service...')


try:
    logger.info('Initializing Redis Sentinel...')
    sentinel = Sentinel(
        [('redis-sentinel-node-0.redis-sentinel-headless.default.svc.cluster.local', 26379),
         ('redis-sentinel-node-1.redis-sentinel-headless.default.svc.cluster.local', 26379),
         ('redis-sentinel-node-2.redis-sentinel-headless.default.svc.cluster.local', 26379)],
        socket_timeout=0.5,
        retry_on_timeout=True,
        decode_responses=True
    )

    redis_master = sentinel.master_for('mymaster', password='YDlHMaWWdI', decode_responses=True, db=0)
    redis_slave = sentinel.slave_for('mymaster', password='YDlHMaWWdI', decode_responses=True, db=1)

    logger.info('Redis Sentinel initialized successfully.')

    # Initialize song and user databases
    songs_db = redis_master
    users_db = redis_master
    
except Exception as e:
    logger.error(f"Redis Sentinel initialization failed: {str(e)}")
    sys.exit(1)
    
# Kafka producer configuration
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

TOPIC_NAME = 'songs'

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

def on_send_success(record_metadata):
    logger.info(f"Message successfully sent to {record_metadata.topic} with offset {record_metadata.offset}")
    
def on_send_error(excp):
    logger.error(f"Error sending message: {excp}")

def send_all_songs_to_kafka():
    logger.info('Sending all songs to Kafka...')
    
    keys = songs_db.keys('song:*')
    
    for key in keys:
        song_data = json.loads(songs_db.get(key).decode('utf-8'))
        producer.send(TOPIC_NAME, value=song_data) 
        logger.info(f"Produced song {song_data['title']} to Kafka topic {TOPIC_NAME}")

    producer.flush()

@app.route('/songs', methods=['POST'])
def add_song():
    SONG_REQUESTS.inc()
    logger.info('Adding song...')
    song_data = request.get_json()
    if not song_data:
        return jsonify({'message': 'Invalid request, no data provided.'}), 400

    try:
        # Deserialize the incoming JSON into a Song object
        song = Song.from_dictionary(song_data)
        
        songs_db.set(f'song:{song.title}', json.dumps(song.to_dict()))
        logger.info(f"Set song in DB: {song.title}")
        logger.info(f"Song in DB after set: {songs_db.get(f'song:{song.title}')}")

        producer.send('songs', key=str(song.title).encode('utf-8'), value=song.to_dict()).add_callback(on_send_success).add_errback(on_send_error)
        producer.flush()

        logger.info(f"Produced new song {song.title} to Kafka topic 'songs'")
        song_key = f'song:{song.title}'
        logger.info(f"Attempting to retrieve song with key: {song_key}")
        song_data = songs_db.get(song_key)
        logger.info(f"Song data retrieved: {song_data}")
        logger.info(f"Current songs in DB: {songs_db.keys()}")
        return jsonify(song.to_dict()), 201

    except Exception as e:
        logger.error(f"Error adding song: {str(e)}")
        return jsonify({'message': f'Failed to add song: {str(e)}'}), 500

@app.route('/users', methods=['POST'])
def add_user():
    USER_REQUESTS.inc()
    logger.info('add user method called')
    user_data = request.get_json()
    if not user_data:
        return jsonify({'message': 'Invalid request'}), 400
    username = user_data['username']
    users_db.set(f'user:{username}', json.dumps(user_data))
    producer.send('users', key=username.encode('utf-8'), value=user_data)
    producer.flush()
    return jsonify(user_data), 201

@app.route('/liveness')
def liveness():
    logger.debug("Liveness probe accessed")
    return jsonify(status="alive"), 200

@app.route('/readiness')
def readiness():
    logger.debug("Readiness probe accessed")
    # Add any necessary checks here
    return jsonify(status="ready"), 200

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    USER_REQUESTS.inc()
    logger.info(f'get user method called with username {username}')
    user_data = users_db.get(f'user:{username}')
    if not user_data:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(json.loads(user_data.decode('utf-8'))), 200

if __name__ == '__main__':
    try:
        logger.info('Starting Flask application...')
        app.run(
            host='0.0.0.0',
            port=443,
            ssl_context=('certs/cert.pem', 'certs/key.pem'),
            debug=True
        )
    except Exception as e:
        logger.error(f'Failed to start Flask application: {str(e)}')
        sys.exit(1)