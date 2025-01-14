import json
from google.cloud import firestore
from datetime import datetime


class DAO(object):
    def __init__(self):
        self.db = firestore.Client()

    ## clean (tested)
    def clean_db(self):
        try:
            ref=self.db.collection('letture')
            for doc in ref.list_documents():
                doc.delete()
            another_ref=self.db.collection('bollette')
            for doc in another_ref.list_documents():
                doc.delete()
        except Exception as e:
            print("Exception cought in clean_db(): {" + str(e) + "}")

    ## read 
    def get_lettura(self, data):
        h = self.db.collection('letture').document(str(data)).get()
        rv = h.to_dict() if h.exists else None
        if rv is not None:
            return {"value":rv['value'],"isInterpolated":False}
        else: return None
    
    def get_lettura_interpolation(self,data):
        lettura = self.get_lettura(data)
        if lettura is not None:
            return lettura
        else:
            items = self.db.collection("letture").order_by('data', direction=firestore.Query.DESCENDING).limit(2).stream()
            rv = [item.to_dict() for item in items if item.exists]
            if len(rv) == 0:
                return {"value":0,"isInterpolated":True}
            elif len(rv) == 1:
                return {"value":rv[0]["value"],"isInterpolated":True}
            elif len(rv)==2:
                t1=self.date_from_str(rv[1]["data"])
                t2=self.date_from_str(rv[0]["data"])
                tx=self.date_from_str(data)
                c1=rv[1]["value"]
                c2=rv[0]["value"]
                print(f'{t1}: {c1}')
                print(f'{t2}: {c2}')
                print(f'{tx}')
                return {"isInterpolated":True,"value":self.interpolation(c1,c2,t1,t2,tx)}
    
    def date_from_str(self,d):
        try: return datetime.strptime(d,'%d-%m-%Y')
        except: return None
    
    def interpolation(self,c1,c2,t1,t2,tx):
        timedelta_21=(t2-t1).total_seconds()
        timedelta_x2=(tx-t2).total_seconds()
        diff=c2-c1 
        return c2 + (diff)*(timedelta_x2)/timedelta_21
    
    def add_lettura(self,data,value):
        item_ref=self.db.collection('letture')
        item_ref.document(data).set({'data': data, 'value': value})
    
    def get_last_bollette(self):
        try:
            items = self.db.collection("bollette").order_by('ultima_lettura', direction=firestore.Query.DESCENDING).limit(12).stream()
            rv = [
                {**item.to_dict(), 'id': item.id} 
                for item in items if item.exists
            ]
            return rv
        except:
            return None
    
    def get_bolletta(self, data):
        h = self.db.collection('bollette').document(str(data)).get()
        rv = h.to_dict() if h.exists else None
        return rv   
    
    
    
