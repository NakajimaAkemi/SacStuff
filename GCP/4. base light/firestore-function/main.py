from google.cloud import firestore

def my_function(event_data,context):
    db = firestore.Client(database='sac-db')
    new_value = event_data['value']['fields']
    data_nuova_lettura = new_value['documentId']['stringValue']
    valore_nuova_lettura = int(new_value['value']['integerValue'])
    costo_nuova_lettura = valore_nuova_lettura * 0.5

    item_ref = db.collection('item').document('identifier')
    if not item_ref.get().exists:
        item_ref.set({
        "consumi": valore_nuova_lettura,
        "costo_complessivo": costo_nuova_lettura,
        "letture": [valore_nuova_lettura]
    })
    else:
        item_ref.update({
            "consumi": firestore.Increment(valore_nuova_lettura),
            "costo_complessivo": firestore.Increment(costo_nuova_lettura),
            "letture": firestore.ArrayUnion([valore_nuova_lettura])
        })

