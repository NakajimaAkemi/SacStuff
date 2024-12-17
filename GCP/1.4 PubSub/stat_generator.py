#!/usr/bin/python3
from google.cloud import firestore
import numpy as np

def get_stats(document):
    v=[float(document[k]) for k in document.keys() ]
    print(v)
    return {
        'count': len(v),
        'avg': np.mean(v),
        'std': np.std(v),
        'min': np.min(v),
        'max': np.max(v),
    }

if __name__=='__main__':
    db = firestore.Client()
    docname='20221013'
    doc=db.collection('temperature').document(docname).get()
    stats=get_stats(doc.to_dict())
    print(stats)
    db.collection('temperature_stats').document(docname).set(stats)

