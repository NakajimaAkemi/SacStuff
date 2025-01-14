import base64
import json
#from google.cloud import firestore

def my_function(event_data, context):
    try:
        # Decodifica del messaggio base64
        pubsub_message = base64.b64decode(event_data['data']).decode('utf-8')
        #pubsub_message = event_data['data'].decode('utf-8')
        # Se il messaggio è in formato JSON, fai il parsing
        #message_data = json.loads(pubsub_message)
        
        #print("Messaggio Pub/Sub decodificato:", message_data)
        #db = firestore.Client()
        #item_ref = db.collection('item').document('identifier').set({"value":pubsub_message})
        # Ora puoi accedere ai dati del messaggio
        # Ad esempio, se il messaggio ha una chiave "name":
        if "name" in message_data:
            print(f"Nome trovato nel messaggio: {message_data['name']}")
        
    except Exception as e:
        print(f"Errore nel parsing del messaggio: {e}")
