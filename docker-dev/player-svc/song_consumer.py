from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
from Song import Song 
import json
import logging
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

TOPIC_NAME = 'songs'
RETRY_INTERVAL = 5
MAX_RETRIES = 5
songs_data = {}

def create_consumer():
    for attempt in range(MAX_RETRIES):
        try:
            consumer = KafkaConsumer(
                TOPIC_NAME,  # Subscribe to topic directly
                bootstrap_servers='kafka:9092',
                group_id='song-group',
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                session_timeout_ms=30000,
                heartbeat_interval_ms=10000,
                max_poll_interval_ms=300000,
                request_timeout_ms=31000
            )
            return consumer
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_INTERVAL)
    return None

def consume_songs():
    logger.info("Consumer thread starting...")
    while True:
        consumer = None
        try:
            consumer = create_consumer()
            if not consumer:
                logger.error("Failed to create consumer")
                time.sleep(RETRY_INTERVAL)
                continue

            logger.info("Starting to consume messages...")
            logger.debug(f"Current cache state: {songs_data}")
            
            for message in consumer:
                try:
                    song_dict = message.value
                    
                    # Use title as key for storage
                    title = song_dict.get('title')
                    if title:
                        # Store the song data directly
                        songs_data[title] = song_dict
                        logger.info(f"Updated cache with song: {title}")
                        logger.debug(f"Cache size: {len(songs_data)}")
                except Exception as e:
                    logger.error(f"Message processing error: {e}", exc_info=True)
                    
        except Exception as e:
            logger.error(f"Consumer error: {e}", exc_info=True)
        finally:
            if consumer:
                consumer.close()
            time.sleep(RETRY_INTERVAL)

def get_songs():
    logger.debug(f"Current songs in storage: {songs_data}")
    return list(songs_data.values())

def get_song(song_title):
    """Get song by title from cache"""
    logger.debug(f"Looking for song: {song_title}")
    logger.debug(f"Available songs: {songs_data}")
    
    # Direct lookup by title
    if song_title in songs_data:
        return songs_data[song_title]
        
    # Case-insensitive search
    song_title_lower = song_title.lower()
    for title, song in songs_data.items():
        if title.lower() == song_title_lower:
            return song
            
    logger.error(f"No song found with title: {song_title}")
    return None