# Deploying Flask app with Firestore DB
In this exercise we will setup a Flask Application backed by a Firestore DB.

## Firestrore DB
Firestore DB is a schema less Database which can store different documents within the same collections, where Each document is uniquely identified by a name. In our Flask application we need to include `google-cloud-firestore` library.

### Setting up the Project and the datastore
We setup a project as usual.

*Linux*
```bash
gcloud app create --project=${PROJECT_ID}
```
*Windows*
```bash
gcloud app create --project=%PROJECT_ID%
```

After doing so we create a database in the Firestore section, making sure to set it up in `Native mode`.
> [!WARNING]
> Keep the database name (default) otherwise it won't be seen

### Setting up the credentials
*Linux*
```bash
export NAME=webuser
export PROJECT_ID=rlfirestore2024
gcloud iam service-accounts create ${NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/owner"
touch credentials.json
gcloud iam service-accounts keys create credentials.json --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```
*Windows*
```bash
set NAME=webuser
set PROJECT_ID=rlfirestore2024
gcloud iam service-accounts create %NAME%
gcloud projects add-iam-policy-binding %PROJECT_ID% --member "serviceAccount:%NAME%@%PROJECT_ID%.iam.gserviceaccount.com" --role "roles/owner"
echo. > credentials.json
gcloud iam service-accounts keys create credentials.json --iam-account %NAME%@%PROJECT_ID%.iam.gserviceaccount.com
set GOOGLE_APPLICATION_CREDENTIALS=%cd%\credentials.json
```

> [!WARNING]
> Remember to include credentials.json to the .gcloudignore file

### Managing data with the Firestore library
*Importing the libary and setting up the connection to the DB*
```Python 
from google.cloud import firestore
client = firestore.Client()
```
*Adding data to the collection*
```Python 
sidious_ref = db.collection('sith').document('dsidious')
sidious_ref.set({
    'first': 'Sheev',
    'last': 'Palpatine',
    'nick': 'Darth Sidious',
    'born': '83 BBY'
})
```
*Reading data*
```Python
def print_stream(docs):
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

sith_ref = db.collection('sith')
docs = sith_ref.stream()
print_stream(docs)
```
*Updating data*
```Python
print_stream(docs)
sith_ref = db.collection('sith').document('dsidious')
sith_ref.update({'born': '84 BBY'})
docs = db.collection('sith').where('first', '==','Sheev').stream()
print_stream(docs)
```
*Querying data*
```Python
docs = db.collection('sith').where('first', '==','Sheev').stream()
print_stream(docs)
## Ordering by and adding a limit
docs = db.collection('sith').order_by('first').limit(2).stream()
print_stream(docs)
docs = db.collection('sith').order_by('first', direction=firestore.Query.DESCENDING).limit(2).stream()
print_stream(docs)
```

### DAO
To manage our data we will use the DAO pattern, which will allow us to define a Model for our data and create a separation with the controller logic. The following code example keeps a collection locally, in order to use the Firestore DB we will need to include the library and adapt our code, as you can see in the `horses_gcp.py` file.

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

### Parsing data in a Flask view
Flask allows us to reference the variables we passed to our HTML views as recipient by using the `{{}}`.
```HTML
<table>
            <tr><td>Breed:</td><td>{{horse['breed']{{</td></tr>
            <tr><td>Specility:</td><td>{{horse['speciality']}}</td></tr>
            <tr><td>Sex:</td><td>{{horse['sex']}}</td></tr>
</table>
```
Define variables by setting a value, we can also apply a filter like `|count` in order to pass the lenght of a collection instead of its items.
```HTML
{% set ngen = pedigree.keys() | count %}
```
`IF` statements.
```HTML
{% if col%2==0 %}
<-----col is an Even number----->
{% else %}
<-----col is an Odd number----->
{% endif %}
```

We can also iterate over collections.
```HTML
{% for i in range(5) %}
{{ i }} 
{% endfor %}

{% for col in range(pedigree[gen]|count) %}
<--Filter iteration happens here-->
{% endfor %}
```

