from google.cloud import firestore
import datetime
import calendar

def function_firestore(event_data, context):
    db = firestore.Client()
    
    new_value = event_data['value']['fields']
    data_lett = new_value['id']['stringValue']
    valu_lett = new_value['value']['integerValue']

    lettura = {'id': data_lett, 'value': valu_lett, 'isInterpolated': False}
    
    costo_lettura = float(valu_lett) * 0.5

    giorno, mese, anno = data_lett.split('-')
    mes = (int(mese) + 1) % 12 if int(mese) != 11 else int(mese) + 1
    mese_bolletta = f'{mes}-{int(anno)+1 if int(mese) == 12 else anno}'
    periodo_bolletta = month_range(int(anno), int(mese))
    item_ref = db.collection('bollette').document(mese_bolletta)
    if item_ref.get().exists:
        item_ref.update({
            'costo': firestore.Increment(costo_lettura),
            'ultima_lettura': lettura,
            'consumi': firestore.Increment(valu_lett)
        })
    else:
        item_ref.set({
            'mese': mese_bolletta,
            'costo': costo_lettura,
            'ultima_lettura': lettura,
            'consumi': valu_lett,
            'periodo': periodo_bolletta
        })


def month_range(anno:int, mese:int) -> str:
    _, numdays = calendar.monthrange(anno, mese)
    first_day = str_from_date(datetime.date(anno, mese, 1))
    last_day = str_from_date(datetime.date(anno, mese, numdays))
    return f'{first_day} -> {last_day}'

def str_from_date(d):
    return d.strftime("%d-%m-%Y")