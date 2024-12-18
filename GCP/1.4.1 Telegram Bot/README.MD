# Telegram bot pub sub
In this section we will set up a Telegram bot by using the Botfather
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
if __name__ == '__main__':
     app.run(host="127.0.0.1", port=8080, debug=True)
```
