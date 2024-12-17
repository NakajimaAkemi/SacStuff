#!/usr/bin/python3
import os
import json
import datetime
from google.cloud import pubsub_v1
from google.cloud import firestore

subscription_name=os.environ['SUBSCRIPTION_NAME'] if 'SUBSCRIPTION_NAME' in os.environ.keys() else 'cpu_temperature'
project_id=os.environ['PROJECT_ID'] if 'PROJECT_ID' in os.environ.keys()  else 'myprj'

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)
db = firestore.Client()

print(subscription_path)

def save_temperature(data):
        dt=datetime.datetime.fromtimestamp(data['timestamp'])
        docname=dt.strftime('%Y%m%d')
        print(docname, data['temperature'])
        db.collection('temperature').document(docname).set({str(data['timestamp']): data['temperature']}, merge=True)

def callback(message):
    message.ack()
    try:
        save_temperature(json.loads(message.data.decode('utf-8')))
    except:
        pass    

if __name__=='__main__':    
    pull = subscriber.subscribe(subscription_path, callback=callback)
    try:
        pull.result()
    except:
        pull.cancel()
