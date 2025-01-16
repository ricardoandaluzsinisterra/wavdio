from kafka import KafkaConsumer
import threading
import json

users_data = {}

users_consumer = KafkaConsumer(
    'users',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='user-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

def consume_users():
    for msg in users_consumer:
        key = msg.key.decode('utf-8')
        value = msg.value
        users_data[key] = value

users_consumer_thread = threading.Thread(target=consume_users)
users_consumer_thread.start()