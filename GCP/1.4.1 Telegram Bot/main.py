import base64
import json
import os
import datetime
import requests
from flask import Flask, render_template, request
from google.cloud import firestore

app = Flask(__name__)

app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']
app.config['BOT_TOKEN'] = os.environ['BOT_TOKEN']
app.config['CHAT_ID']=None

db = firestore.Client()

def telegram_send(data):
    val=data['temperature'] if 'temperature' in data.keys() else 'too high'
    message= f'temperature is {val}'
    token=app.config['BOT_TOKEN']
    chatid=app.config['CHAT_ID']
    print(token)
    try:
        if chatid is None:
            r=requests.get(f'https://api.telegram.org/bot{token}/getUpdates')
            if r.status_code == 200:
                chatid=r.json()['result'][0]['message']['from']['id']
                app.config['CHAT_ID']=chatid
        requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={'chat_id': chatid, 'text': message})
    except: pass

def save_to_db(data):
    dt=datetime.datetime.fromtimestamp(data['timestamp'])
    docname=dt.strftime('%Y%m%d')
    val=data['temperature'] if 'temperature' in data.keys() else 'alert'
    db.collection('temperature_alert').document(docname).set({str(data['timestamp']): val}, merge=True)

@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
    print('Received pubsub push')
    if request.args.get('token', '') != app.config['PUBSUB_VERIFICATION_TOKEN']:
        return 'Invalid request', 400
    envelope = json.loads(request.data.decode('utf-8'))
    save_to_db(json.loads(base64.b64decode(envelope['message']['data'])))
    telegram_send(json.loads(base64.b64decode(envelope['message']['data'])))
    return 'OK', 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
