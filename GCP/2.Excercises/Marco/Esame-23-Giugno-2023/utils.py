import ipaddress

def isinaddr(ip:str, ip_n:str, nm:int) -> bool:
    try:
        if ipaddress.ip_address(ip) in ipaddress.ip_network(f'{ip_n}/{nm}'):
            return True
        else:
            return False
    except:
        return False
    
def ip_validation(ip:str) -> bool:
    try:
        ipaddress.ip_address(ip)
    except:
        return False
    
    return True