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
                bootstrap_servers='kafka:9092',
                group_id='song-group',
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                session_timeout_ms=30000,  # 30 seconds
                heartbeat_interval_ms=10000,  # 10 seconds
                max_poll_interval_ms=300000,  # 5 minutes
                request_timeout_ms=31000
            )
            
            # Manual topic assignment
            partitions = [TopicPartition(TOPIC_NAME, 0)]
            consumer.assign(partitions)
            
            return consumer
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_INTERVAL)
    return None

def consume_songs():
    while True:
        consumer = None
        try:
            consumer = create_consumer()
            if not consumer:
                logger.error("Failed to create consumer")
                time.sleep(RETRY_INTERVAL)
                continue

            logger.info("Starting to consume messages...")
            for message in consumer:
                try:
                    key = message.key.decode('utf-8') if message.key else None
                    song_dict = message.value
                    song = Song.from_dictionary(song_dict)
                    songs_data[key] = song
                    logger.info(f"Consumed song: {song}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    
        except Exception as e:
            logger.error(f"Consumer error: {e}")
        finally:
            if consumer:
                consumer.close()
            time.sleep(RETRY_INTERVAL)

def get_songs():
    logger.debug(f"Current songs in storage: {songs_data}")
    return list(songs_data.values())