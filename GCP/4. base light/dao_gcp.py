import json
from google.cloud import firestore



class DAO(object):
    def __init__(self):
        self.db = firestore.Client()
        #self.max_id = 0

    ## clean (tested)
    def clean_db(self):
        try:
            ref=self.db.collection('item')
            for doc in ref.list_documents():
                doc.delete()
            #another_ref=self.db.collection('another_item')
            #for doc in another_ref.list_documents():
            #    doc.delete()
        except Exception as e:
            print("Exception cought in clean_db(): {" + str(e) + "}")

    ## read 
    def get_item(self, iditem):
        h = self.db.collection('item').document(str(iditem)).get()
        rv = h.to_dict() if h.exists else None
        return rv
    
    #### list with id
    def get_items_with_identifier(self):
        items = self.db.collection('item').stream()
        rv = [
            {**item.to_dict(), 'id': item.id} 
            for item in items if item.exists
        ]
        return rv
    
    #def get_item(self, iditem):
    #    h = self.db.collection('item').document(str(iditem)).get()
    #    if h.exists:
    #        data = h.to_dict()
    #        data['id'] = h.id  # Add the document ID to the returned data
    #        return data
    #    return None

    ## CREATE OR UPDATE
    ####################
    def add_item(self,iditem,property1,int_property):
        item_ref=self.db.collection('item')
        item_ref.document(str(iditem)).set({'property1': property1, 'int_property': str(int_property)})
        #item_ref.document(str(self.max_id)).set({'property1': property1, 'int_property': str(int_property)})
        #self.max_id = self.max_id + 1
        
    def add_or_update_item(self,iditem,attribute):
        item_ref = self.db.collection('item').document(str(iditem))
        if not item_ref.get().exists:
            item_ref.set({
            "atrtribute": attribute
        })
        else:
            item_ref.update({
                "int_attribute": firestore.Increment(attribute),
                "array": firestore.ArrayUnion([attribute])
            })

    ## update(tested)
    def update_item(self,iditem,property,property2):
        object_ref = self.db.collection('items').document(str(iditem))
        object_ref.update({'property': property,'property2':property2})      
    
    ### Querying
    #################
    ## querying ## (tested)
    def query(self,collection, attribute, operator, value):
        #:: Various operators
            # '=='
            # '!='
            # '>='
            # '<='
            # '>'
            # '<'
            # array_contains
            # array_contains_any
        items = self.db.collection(collection).where(attribute, operator, value).stream()
        rv = [item.to_dict() for item in items if item.exists]
        return rv
    

    ## order by attribute with a top k (tested)
    def get_most_viewed(self,top=4):
        items = self.db.collection('item').order_by('attribute', direction=firestore.Query.DESCENDING).limit(top).stream()
        rv = [item.to_dict() for item in items if item.exists]
        return rv
    
    
    
