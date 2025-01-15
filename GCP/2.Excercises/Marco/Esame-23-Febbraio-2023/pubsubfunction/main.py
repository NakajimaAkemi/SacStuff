from google.cloud import firestore
import base64

def pubsub_function(event_data, context):
    try:
        message_data = base64.b64decode(event_data['data']).decode('utf-8')

        db = firestore.Client()
        if "provola" in message_data:
            item_ref = db.collection('pubsub-message').add({'m': message_data})
        
    except Exception as e:
        print(f"Errore nel parsing del messaggio: {e}")