import os
from time import sleep
from json import dumps, loads
from kafka import KafkaConsumer, KafkaProducer
from random import randint
import math


instanceID = os.environ["instanceID"]

producer = KafkaProducer(
    bootstrap_servers = ['kafka:9092']
    , value_serializer = lambda x: dumps(x).encode('utf-8')
)

consumer = KafkaConsumer(
    'llm-queue-input',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='DUMMY-LLM',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)


for message in consumer:
    print(f'Processed {message.value}', flush=True)
    sleep(randint(10,100) * math.pow(int(instanceID), 4) / 1000)
    producer.send('llm-queue-output', value=f'Message {message.value} processed by {instanceID}')
