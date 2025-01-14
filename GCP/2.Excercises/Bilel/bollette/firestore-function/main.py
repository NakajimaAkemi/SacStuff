from google.cloud import firestore
import calendar 
import datetime

def my_function(event_data,context):
    db = firestore.Client()
    new_value = event_data['value']['fields']
    ultima_lettura = new_value['data']['stringValue']
    valore_nuova_lettura = int(new_value['value']['integerValue'])
    
    costo_nuova_lettura = valore_nuova_lettura * 0.5
    id,periodo = get_mese_anno_successivo(ultima_lettura)
    item_ref = db.collection('bollette').document(str(id))
    if not item_ref.get().exists:
            item_ref.set({
            "data":id,
            "costo": costo_nuova_lettura,
            "ultima_lettura":ultima_lettura,
            "consumi":valore_nuova_lettura,
            "periodo":periodo
    })
    else:
        item_ref.update({
            "costo": firestore.Increment(costo_nuova_lettura),
            "ultima_lettura":ultima_lettura,
            "consumi":firestore.Increment(valore_nuova_lettura),
        })


def get_mese_anno_successivo(data):
    _,mese,anno=data.split('-')
    mese = int(mese)
    anno= int(anno)
    periodo=month_range(anno,mese)
    if mese < 12:
        mese=mese + 1
    else:
        mese=1
        anno=anno+1
    data_ref=str(mese)+"-"+str(anno)
    return data_ref,periodo


def month_range(anno,mese):
    _, num_days=calendar.monthrange(anno, mese)
    first_day = str_from_date(datetime.date(anno, mese, 1))
    last_day = str_from_date(datetime.date(anno, mese, num_days))
    return first_day + "---"+last_day
    
def str_from_date(d):
    return d.strftime("%d-%m-%Y")
    
