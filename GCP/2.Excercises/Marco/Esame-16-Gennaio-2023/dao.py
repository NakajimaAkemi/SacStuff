from google.cloud import firestore
from typing import Optional
from utils import interpolation

class bolletteDao(object):
    def __init__(self):
        self.db = firestore.Client()

    def clean_db(self) -> None:
        try:
            ref=self.db.collection('letture')
            for doc in ref.list_documents():
                doc.delete()
            another_ref=self.db.collection('bollette')
            for doc in another_ref.list_documents():
                doc.delete()
        except Exception as e:
            print(f"Exception cought in clean_db(): {str(e)}")
    
    def check_if_in(self, date:str) -> Optional[dict]:
        h = self.db.collection('letture').document(str(date)).get()
        rv = h.to_dict() if h.exists else None
        return rv

    def get_lettura_by_id(self, date:str) -> Optional[dict]:
        
        rv = self.check_if_in(date)

        if rv is None:
            p = self.get_ready_interpolation(date)
            if p is None:
                rv = {'id': str(date), 'value': 0, 'isInterpolated': True}
            elif len(p) == 1:
                rv = {'id': str(date), 'value': p[0]['value'], 'isInterpolated': True}
            elif len(p) == 2:
                c = interpolation(date, p)
                rv = {'id': str(date), 'value': c, 'isInterpolated': True}

        if rv is not None:
            del rv['id']
        return rv
    
    def add_item_by_id(self, date:str, lettura:dict) -> Optional[dict]:
        ref =self.db.collection('letture')
        ref.document(str(date)).set({'id': str(date), **lettura, 'isInterpolated': False})
        rv = ref.document(str(date)).get().to_dict()
        del rv['id']
        return rv

    
    def get_ready_interpolation(self, date:str) -> Optional[list[dict]]:
        items = self.db.collection('letture').where('id', '<', date).order_by('id', direction=firestore.Query.DESCENDING).limit(2).stream()
        rv = [item.to_dict() for item in items if item.exists]
        if len(rv) == 0:
            return None
        else:
            return rv
        
    def get_last_year_billings(self) -> Optional[list[dict]]:
        items = self.db.collection('bollette').order_by('id', direction=firestore.Query.DESCENDING).limit(12).stream()
        rv = []
        for item in items:
            if item.exists():
                del item['id']
            rv.append(item)

        return rv

    def populate_billing(self, date:str, billing:dict) -> None:
        ref = self.db.collection('bolletta')
        ref.document(date).set({'id': date, **billing})