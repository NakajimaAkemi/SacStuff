from google.cloud import firestore
import json 

class Horses(Object):
      def __init__(self):
            self.db.firestore.Client()
            self.populate_db('horses.json')
      def populate_db(self, filename):
            horses_ref=self.db.collection('horses') 
            with open(filename) as f: 
                horses = json.load(f)
                for h in horses:
                    horses_ref.document(h['name']).set(h)


def print_stream(docs):
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')
            


## Il nostro firestore Client
db = firestore.Client()

## aggiungiamo la collection e oggetti Sith
vader_ref = db.collection('sith').document('dvader')
vader_ref.set({'first': 'Anakin','last': 'Skywalker','nick': 'Darth Vader','born': '41 BBY'})
sidious_ref = db.collection('sith').document('dsidious')
sidious_ref.set({'first': 'Sheev','last': 'Palpatine','nick': 'Darth Sidious','born': '83 BBY'})

## printiamo la collection sith
sith_ref = db.collection('sith')
docs = sith_ref.stream()
print_stream(docs)

## Where clause
docs = db.collection('sith').where('first', '==', 'Sheev').stream()

## Limit e order by clause
docs = db.collection('sith').order_by('first').limit(2).stream()
docs = db.collection('sith').order_by('first', direction=firestore.Query.DESCENDING).limit(2).stream()
print_stream(docs)
## Update
sith_ref = db.collection('sith').document('dsidious')
sith_ref.update({'born': '84 BBY'})
docs = db.collection('sith').where('first', '==', 'Sheev').stream()
print_stream(docs)


