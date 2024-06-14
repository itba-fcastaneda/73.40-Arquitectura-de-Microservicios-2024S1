import uvicorn
import logging
import sqlite3
import threading
from fastapi import FastAPI
from time import sleep, time
from json import dumps, loads
from collections import namedtuple
from kafka import KafkaProducer, KafkaConsumer

def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)

db = '/etc/example.db'
conn = sqlite3.connect(db)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS requests
            (
               id INTEGER PRIMARY KEY, name TEXT
               , inventory INTEGER, payment INTEGER, shipping INTEGER
            )''')

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers = ['kafka:9092']
    , value_serializer = lambda x: dumps(x).encode('utf-8')
)
consumer = KafkaConsumer(
    'ms-response',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='API',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

class BackgroundTasks(threading.Thread):

    def update_req(self, msg):
        cursor = self.conn.cursor()
        status = 1 if msg['status'] == 'ok' else -1
        cursor.execute(f"UPDATE requests SET {msg['service']} = ? WHERE id = ?", (status, msg['ID']))
        self.conn.commit()

    def check(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * from requests WHERE id = ?", (id, ))
        row = cursor.fetchone()
        if row.shipping == 0 or row.payment == 0 or row.inventory == 0:
            return 0
        if row.shipping == -1 or row.payment == -1 or row.inventory == -1:
            return -1
        if row.shipping == 1 and row.payment == 1 and row.inventory == 1:
            return 1
        return 0

    def commit(self, id):
        data = {'ID' : id, 'action': 'commit'}
        producer.send('ms-request', value=data)

    def rollback(self, id):
        data = {'ID' : id, 'action': 'rollback'}
        producer.send('ms-request', value=data)
    

    status_msg = {
        0: 'WAITING'
        , 1: 'COMMIT'
        , -1: 'ROLLBACK'
    }

    def run(self,*args,**kwargs):
        self.conn = sqlite3.connect(db)
        self.conn.row_factory = namedtuple_factory
        while True:
            for _, values in consumer.poll(timeout_ms=1000).items():
                for v in values:
                    id = v.value['ID']
                    self.update_req(v.value)
                    status = self.check(id)
                    print(f'Order {v.value} is {self.status_msg[status]}', flush=True)
                    if status == 1:
                        self.commit(id)
                    elif status == -1:
                        self.rollback(id)



@app.get("/order/{name}")
def read_root(name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO requests (name, inventory, payment, shipping) VALUES (?, ?, ?, ?)", (name, 0, 0, 0))
    id = cursor.lastrowid
    conn.commit()

    data = {'ID' : id, 'name': name, 'action': 'new'}
    producer.send('ms-request', value=data)
    return {'ID' : id, 'name': name}


if __name__ == '__main__':
    t = BackgroundTasks()
    t.start()
    logging.getLogger("uvicorn").handlers.clear()
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.disabled = True
    uvicorn.run(app, host="0.0.0.0", port=8000)