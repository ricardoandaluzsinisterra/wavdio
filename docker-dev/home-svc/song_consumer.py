import time
from kafka import KafkaConsumer
import json
import Song  # Assuming Song class is in this file
import logging

logging.basicConfig(filename='consumer.log', level=logging.INFO)

consumer = KafkaConsumer(
    'songs',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id='song-consumer-group',
    auto_offset_reset='earliest'
)

songs = []

def consume_songs():
    global songs
    while True:
        new_songs = []
        for message in consumer:
            song_dict = message.value
            song = Song.from_dict(song_dict) 
            new_songs.append(song)
        
        if new_songs:
            songs.extend(new_songs)
            logging.info(f"Fetched {len(new_songs)} new songs")

        time.sleep(15)

def get_songs():
    global songs
    return songs
