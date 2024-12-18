# Telegram bot pub sub
In this section we will set up a Telegram bot by using the Botfather, first of all we 
```python
#!/usr/bin/python
import base64
import json
import os
import datetime
from flask import Flask, render_template, request
from google.cloud 
import firestore
app = Flask(__name__)
app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']
app.config['BOT_TOKEN'] = os.environ['BOT_TOKEN']
app.config['CHAT_ID']=None
db = firestore.Client()

@app.route('/pubsub/push', methods=['POST'])
     def pubsub_push():
               print('Received pubsub push')
               if request.args.get('token', '') != app.config['PUBSUB_VERIFICATION_TOKEN']:
                   return 'Invalid request', 404envelope = json.loads(request.data.decode('utf-8'))
               data=json.loads(base64.b64decode(envelope['message']['data']))
               save_to_db(data)
               telegram_send(data)
               return 'OK', 200


if __name__ == '__main__':
     app.run(host="127.0.0.1", port=8080, debug=True)
```
