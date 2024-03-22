import os
from time import sleep
from json import dumps, loads
from kafka import KafkaConsumer, KafkaProducer
from random import randint
import math

app_name = os.environ["APP_NAME"]

consumer = KafkaConsumer(
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=app_name,
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

consumer.subscribe(['users-login','users-logout'])

while True:
    for topic, values in consumer.poll(timeout_ms=1000).items():
        for v in values:
            print(f'Message from topic [{topic.topic}]: [{v.value}]', flush=True)