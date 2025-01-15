from google.cloud import firestore
from utils import generate_id, get_hashtags, generate_timestamp
from typing import Optional

class chirpsDAO(object):
    def __init__(self):
        self.db = firestore.Client()

    def clean_db(self) -> None:
        try:
            ref=self.db.collection('messages')
            for doc in ref.list_documents():
                doc.delete()
            another_ref=self.db.collection('hashtags')
            for doc in another_ref.list_documents():
                doc.delete()
        except Exception as e:
            print(f"Exception caught in clean_db(): {str(e)}")

    def get_chirp_by_id(self, id:str) -> Optional[dict]:
        h = self.db.collection('messages').document(id).get()
        rv = h.to_dict() if h.exists else None
        if rv is not None:
            rv['id'] = ''
            rv['timestamp'] = ''
        return rv
    
    def add_new_chirp(self, message:str) -> Optional[dict]:
        item_ref=self.db.collection('message')
        id = generate_id()
        timestamp = generate_timestamp()
        item_ref.document(id).set({'id': id, 'message': message, 'timestamp': timestamp})

        hashtags = get_hashtags(message)
        item_ref_h = self.db.collection('hashtags')
        for hashtag in hashtags:
            item_ref_h.document(hashtag).set({'document_id': id, 'timestamp': timestamp})
        return item_ref.document(id).get().to_dict()

    def get_hashtag(self, hashtag:str) -> list[dict]:

        item_ref=self.db.collection('hashtags')
        rv = item_ref.document(hashtag).get()
        h = rv.to_dict() if rv.exists else None
        rv = self.db.collection('message').document(h['document_id']).get()
        h = rv.to_dict() if rv.exists else None
        return h
