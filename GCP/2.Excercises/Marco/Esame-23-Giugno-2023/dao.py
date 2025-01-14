from google.cloud import firestore
from typing import Optional
from utils import isinaddr

db = firestore.Client()

class routingDAO(object):

    def clean_db() -> None:
        try:
            ref= db.collection('table')
            for doc in ref.list_documents():
                doc.delete()
        except Exception as e:
            print("Exception caught in clean_db(): {" + str(e) + "}")

    def get_rule_from_id(id:int) -> Optional[dict]:
        h = db.collection('table').document(id).get()
        rv = h.to_dict() if h.exists else None
        return rv
    
    def add_rule_on_id(id:int, rule:dict) -> Optional[dict]:
        db.collection('table').document(id).set(rule)
        return db.collection('table').document(id).get().to_dict()
    
    def edit_rule_on_id(id:int, rule:dict) -> Optional[dict]:
        db.collection('table').document(id).update(rule)
        return db.collection('table').document(id).get().to_dict()
    
    def delete_rule_by_id(id:int) -> None:
        db.collection('table').document(id).delete()

    def get_table() -> list[str]:
        items = db.collection('table').order_by('netmaskCIDR', direction=firestore.Query.DESCENDING).stream()
        rv = [str(item.id) for item in items]
        if len(rv) == 0:
            return None
        else:
            return rv
    
    def get_table_with_attr() -> list[dict]:
        items = db.collection('table').order_by('netmaskCIDR', direction=firestore.Query.DESCENDING).stream()
        rv = [{'id': str(item.id), **item.to_dict()} for item in items]
        if len(rv) == 0:
            return None
        else:
            rv_sorted = sorted(rv, key=lambda d: d['id'])
            return rv_sorted

    def post_item(ip:str):
        items = db.collection('table').order_by('netmaskCIDR', direction=firestore.Query.DESCENDING).stream()
        ip_l = [{'id': str(item.id), **item.to_dict()} for item in items]

        for i in ip_l:
            if isinaddr(ip, i['ip'], i['netmaskCIDR']):
                return i['id']
        
        return None
            

    
    
    

