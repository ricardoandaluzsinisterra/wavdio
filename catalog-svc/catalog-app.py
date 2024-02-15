from flask import Flask, jsonify, request
import redis
import json

app = Flask(__name__)

songs_db = redis.Redis(host='songs-db', port=6379, db=0)
users_db = redis.Redis(host='users-db', port=6379, db=0)

@app.route('/songs', methods=['GET'])
def get_songs():
    title = request.args.get('title')
    if title:
        keys = songs_db.keys(f'song:*:{title}')
    else:
        keys = songs_db.keys('song:*')
    data = {key.decode('utf-8'): json.loads(r.get(key).decode('utf-8')) for key in keys}
    return jsonify(data), 200

@app.route('/songs', methods=['POST'])
def add_song():
    song_data = request.get_json()
    if not song_data:
        return jsonify({'message': 'Invalid request'}), 400
    r.set(f'song:{song_data["id"]}', json.dumps(song_data))
    return jsonify(song_data), 201

@app.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    song_data = songs_db.get(f'song:{song_id}')
    if not song_data:
        return jsonify({'message': 'Song not found'}), 404
    return jsonify(json.loads(song_data.decode('utf-8'))), 200

@app.route('/users', methods=['POST'])
def add_user():
    user_data = request.get_json()
    if not user_data:
        return jsonify({'message': 'Invalid request'}), 400
    users_db.set(f'user:{user_data["username"]}', json.dumps(user_data))
    return jsonify(user_data), 201

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user_data = users_db.get(f'user:{username}')
    if not user_data:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(json.loads(user_data.decode('utf-8'))), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)