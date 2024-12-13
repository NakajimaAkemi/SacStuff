import json

class Horses(object):
    def __init__(self):
        self.populate_db('horses.json')

    def populate_db(self, filename):
        self.horses_db={}
        print(filename)
        with open(filename) as f:
            horses = json.load(f)
        for h in horses:
            self.horses_db[h['name']]=h

    def get_parents(self, horses_list):
        rv=[]
        for name in horses_list:
            if name in self.horses_db.keys():
                h=self.horses_db[name]
                rv.append(h['sire'] if 'sire' in h.keys() else '')
                rv.append(h['dam'] if 'dam' in h.keys() else '')
                pass
            else:
                rv.extend(['', ''])
        return rv
    
    def get_horse(self, name):
        name=name.upper()
        if name in self.horses_db.keys():
            return self.horses_db[name]
        else:
            return None

    def get_pedigree(self, name, ngen=2):
        name=name.upper()
        horses_list=[name]
        pedigree={}
        for i in range(ngen):
            pedigree[i]=horses_list
            horses_list=self.get_parents(horses_list)
        return pedigree



'''if __name__ == '__main__':
     h=Horses()
     h.populate_db("horses.json")
     print(h.get_horse('Varenne'))'''