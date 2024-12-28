import json
from google.cloud import firestore



class DAO(object):
    def __init__(self):
        self.db = firestore.Client()
        self.populate_item('item.json')

    ## populate (tested)
    def populate_item(self, filename):
        item_ref=self.db.collection('item')
        with open(filename) as f:
            items = json.load(f)
            for item in items:
                item_ref.document(str(item['id'])).set({'property1': item['property1'], 'int_property': str(item['int_property'])})
    
    ## clean (tested)
    def clean_db(self):
        try:
            ref=self.db.collection('item')
            for doc in ref.list_documents():
                doc.delete()
            another_ref=self.db.collection('another_item')
            for doc in another_ref.list_documents():
                doc.delete()
        except Exception as e:
            print("Exception cought in clean_db(): {" + str(e) + "}")

    ## read 
    def get_item(self, iditem):
        h = self.db.collection('item').document(str(iditem)).get()
        rv = h.to_dict() if h.exists else None
        return rv
    
    ## create (tested)
    def add_item(self,iditem,property1,int_property):
        umarell_ref=self.db.collection('umarell')
        umarell_ref.document(str(iditem)).set({'property1': property1, 'int_property': str(int_property)})
    
    ## update(tested)
    def update_item(self,iditem,property,property2):
        object_ref = self.db.collection('items').document(str(iditem))
        object_ref.update({'property': property,'property2':property2})      
    
        
    ## delete (tested)
    def delete_item(self,iditem):
        ref = self.db.collection('collection_name'); 
        doc = ref.document(str(iditem)).get()  
        if doc.exists:     
            print(f'Document data: {doc.to_dict()}')     
            doc.reference.delete() 
        else:     
            print('No such document!')
    


    ## querying ## (tested)
    def query(self,collection, attribute, operator, value):
        #:: Various operators
            # '=='
            # '!='
            # '>='
            # '<='
            # '>'
            # '<'
        items = self.db.collection(collection).where(attribute, operator, value).stream()
        rv = [item.to_dict() for item in items if item.exists]
        return rv
    
    
    ## increment (tested)
    def increase_attribute(self,iditem):
        name=name.upper()
        self.db.collection('item').document(str(iditem)).update({"attribute": firestore.Increment(1)})

    ## order by attribute with a top k (tested)
    def get_most_viewed(self,top=4):
        items = self.db.collection('item').order_by('attribute', direction=firestore.Query.DESCENDING).limit(top).stream()
        rv = [item.to_dict() for item in items if item.exists]
        return rv
    
    
    def get_items_with_identifier(self):
        items = self.db.collection('item').stream()
        rv = [
            {**item.to_dict(), 'id': item.id} 
            for item in items if item.exists
        ]
        return rv
