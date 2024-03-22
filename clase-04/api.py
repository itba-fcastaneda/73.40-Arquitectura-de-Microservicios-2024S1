from time import sleep, time
from json import dumps, loads
from kafka import KafkaProducer, KafkaConsumer
import threading
from fastapi import FastAPI
import uvicorn
import logging

app = FastAPI()
producer = KafkaProducer(
    bootstrap_servers = ['kafka:9092']
    , value_serializer = lambda x: dumps(x).encode('utf-8')
)
consumer = KafkaConsumer(
    'llm-queue-output',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='API',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)


class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            for _, values in consumer.poll(timeout_ms=1000).items():
                for v in values:
                    print(v.value, flush=True)


@app.get("/chat/{msg}")
def read_root(msg):
    data = {'TIME' : time(), 'MSG': msg}
    producer.send('llm-queue-input', value=data)
    return

@app.get("/login/{user}")
def read_root(user):
    data = {'TIME' : time(), 'MSG': f'login user=[{user}]'}
    producer.send('users-login', value=data)
    return

@app.get("/logout/{user}")
def read_root(user):
    data = {'TIME' : time(), 'MSG': f'logout user=[{user}]'}
    producer.send('users-logout', value=data)
    return


if __name__ == '__main__':
    t = BackgroundTasks()
    t.start()
    logging.getLogger("uvicorn").handlers.clear()
    uvicorn.run(app, host="0.0.0.0", port=8000)