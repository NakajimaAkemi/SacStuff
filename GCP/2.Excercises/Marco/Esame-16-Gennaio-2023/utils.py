from datetime import datetime

def date_from_str(d:str) -> datetime:
    try: 
        return datetime.strptime(d, '%d-%m-%Y')
    except: 
        return None
    
def str_from_date(d:datetime) -> str:
    return d.strftime('%d-%m-%Y')

def interpolation(d:str, l:list[dict]) -> int:

    t1 = date_from_str(l[0]['id'])
    t2 = date_from_str(l[1]['id'])
    c1 = l[0]['value']
    c2 = l[1]['value']
    tx = date_from_str(d)
    delta_now = (tx - t2).total_seconds()
    delta = (t2 - t1).total_seconds()
    
    print(f'{t1}: {c1}')
    print(f'{t2}: {c2}')
    print(f'{tx}')
    cx = c2 + ((delta_now/delta) * (c2 - c1))

    return round(cx)