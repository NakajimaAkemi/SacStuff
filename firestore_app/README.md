# Deploying Flask app with Firestore DB
In this exercise we will setup a Flask Application backed by a Firestore DB.

## Firestrore DB
Firestore DB is a schema less Database which can store different documents within the same collections, where Each document is uniquely identified by a name. In our Flask application we need to include `google-cloud-firestore` library.

### Setting up the credentials
*Linux*
```bash
export NAME=webuser
export PROJECT_ID=rlfirestore2024
gcloud iam service-accounts create ${NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com"--role "roles/owner"touch credentials.json
gcloud iam service-accounts keys create credentials.json --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```
*Windows*
```bash
set NAME=webuser
set PROJECT_ID=rlfirestore2024
gcloud iam service-accounts create ${NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com"--role "roles/owner"touch credentials.json
gcloud iam service-accounts keys create credentials.json --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```
### Managing data with the Firestore library
```
```
### DAO
To manage our data we will use the DAO pattern, which will allow us to define a Model for our data and create a separation with the controller logic.
```python
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
```
