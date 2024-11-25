import json
from google.cloud import firestore

class Horses(object):
    def __init__(self):
        self.db = firestore.Client()
        self.populate_db('horses.json')

    def populate_db(self, filename):
        horses_ref=self.db.collection('horses')
        with open(filename) as f:
            horses = json.load(f)
        for h in horses:
            horses_ref.document(h['name']).set(h)

    def get_horse(self, name):
        name=name.upper()
        if name == '':
            return None
        h = self.db.collection('horses').document(name).get()
        rv = h.to_dict() if h.exists else None
        return rv

    def get_parents(self, horses_list):
        rv=[]
        for name in horses_list:
            h=self.get_horse(name)
            if h is not None:
                rv.append(h['sire'] if 'sire' in h.keys() else '')
                rv.append(h['dam'] if 'dam' in h.keys() else '')
            else:
                rv.extend(['',''])
        return rv
    
    def get_pedigree(self, name, ngen=2):
        name=name.upper()
        horses_list=[name]
        pedigree={}
        for i in range(ngen):
            pedigree[i]=horses_list
            horses_list=self.get_parents(horses_list)
        return pedigree

if __name__ == '__main__':
    h = Horses()
    print(h.get_horse('VARENNE'))
    print(h.get_parents('VARENNE'))
    print(h.get_pedigree('VARENNE', ngen=4))
