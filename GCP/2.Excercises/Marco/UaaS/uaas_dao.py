from google.cloud import firestore
import json

class Uaas(object):
    
    def __init__(self):
        self.db = firestore.Client()
        #self.populate_db()
        
    def add_umarell(self, id:int, nome:str, cognome:str, cap:int):
        ref = self.db.collection('umarell')
        ref.document(f'{id}').set({'nome': nome, 'cognome': cognome, 'cap': cap})
    
    def add_cantiere(self, id:int, indirizzo:str, cap:int):
        ref = self.db.collection('cantiere')
        ref.document(f'{id}').set({'indirizzo':indirizzo, 'cap':cap})
        
    def get_umarell_by_id(self, id:int) -> dict:
        return self.db.collection('umarell').document(f'{id}').get().to_dict()
    
    def get_cantiere_by_id(self, id:int) -> dict:
        return self.db.collection('cantiere').document(f'{id}').get().to_dict()
    
#    def populate_db(self):
#        with open('umarell.json') as f:
#            data = json.load(f)
#            for d in data:
#                self.add_umarell(d['id'], d['nome'], d['cognome'], d['cap'])
#               
#        with open('cantiere.json') as f2:
#           data2 = json.load(f2)
#           for d in data2:
#               self.add_cantiere(d['id'], d['indirizzo'], d['cap'])
    
    def clear_db(self):
        ref = self.db.collection('umarell').list_documents()
        for doc in ref:
            doc.delete()
        ref = self.db.collection('cantiere').list_documents()
        for doc in ref:
            doc.delete()
    