import os
from time import sleep
from json import dumps, loads
from kafka import KafkaConsumer, KafkaProducer
from random import randint
import math

instanceID = int(os.environ["instanceID"])
service = os.environ["serviceName"]

producer = KafkaProducer(
    bootstrap_servers = ['kafka:9092']
    , value_serializer = lambda x: dumps(x).encode('utf-8')
)

consumer = KafkaConsumer(
    'ms-request',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=service,
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)


for message in consumer:
    # sleep(randint(10,100) * math.pow(instanceID, 4) / 1000)
    if message.value['action'] == 'new':
        status = 'ok'
        if randint(1,100) > (90 + 3*instanceID):
            status = 'error'
            print(f'Rejecting {message.value}', flush=True)
        data = {'ID': message.value['ID'], 'service': service, 'status': status}
        producer.send('ms-response', value=data)
    elif message.value['action'] == 'commit':
        print(f'COMMIT {message.value}', flush=True)
    elif message.value['action'] == 'rollback':
        print(f'ROLLBACK {message.value}', flush=True)
