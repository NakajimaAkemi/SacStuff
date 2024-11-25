from google.cloud import firestore
db = firestore.Client()


# populate db
vader_ref = db.collection('sith').document('dvader')
vader_ref.set({
    'first': 'Anakin',
    'last': 'Skywalker',
    'nick': 'Darth Vader',
    'born': '41 BBY'
})
sidious_ref = db.collection('sith').document('dsidious')
sidious_ref.set({
    'first': 'Sheev',
    'last': 'Palpatine',
    'nick': 'Darth Sidious',
    'born': '83 BBY'
})
maul_ref = db.collection('sith').document('dmaul')
maul_ref.set({
    'first': 'Maul',
    'last': 'Opress',
    'nick': 'Darth Maul',
    'born': '54 BBY'
})

# read data
print("*** Read data ***")
def print_stream(docs):
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

sith_ref = db.collection('sith')
docs = sith_ref.stream()
print_stream(docs)

# update
print("*** Update dsidious ***")
sith_ref = db.collection('sith').document('dsidious')
sith_ref.update({'born': '84 BBY'})

# query 
print("*** Query ***")
docs = db.collection('sith').where('first', '==', 'Sheev').stream()
print_stream(docs)

# ordering and limiting
print("*** Ordering ASCENDING ***")
docs = db.collection('sith').order_by('first').limit(2).stream()
print_stream(docs)

print("*** Ordering DESCENDING ***")
docs = db.collection('sith').order_by('first', direction=firestore.Query.DESCENDING).limit(2).stream()
print_stream(docs)

print("*** Complex ordering ***")
# need to create index
docs = db.collection('sith').order_by('first').order_by('nick').stream()
print_stream(docs)
