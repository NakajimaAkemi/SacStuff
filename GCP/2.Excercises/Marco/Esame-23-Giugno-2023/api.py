from flask import Flask, request
from flask_restful import Resource
from typing import Optional
from dao import routingDAO
import ipaddress

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static'
            )

class routingIDResource(Resource):
    def validate_id(self, id: Optional[int]) -> bool:
        try: 
            ident = int(id)
        except:
            return False
        
        if ident < 0:
            return False
        return True 
    
    def validate_ip(self, ip:str, netmask:int) -> bool:
        complete_ip = f'{ip}/{str(netmask)}'
        try:
            ipaddress.ip_network(complete_ip)
        except:
            print(f'Eccezione cacciata su {complete_ip}, non ringraziarmi')
            return False
        return True
    
    def validate_gw(self, gw:str)-> bool:
        octs = gw.split('.')
        if len(octs) > 4:
            return False
        
        try:
            ipaddress.ip_address(gw)
        except:
            return False
        return True
    
    def validate_data(self, data:dict) -> bool:
        for k in ['ip', 'netmaskCIDR', 'gw', 'device']:
            if k not in data.keys():
                return False
        
        ip = data['ip']
        nm = data['netmaskCIDR']
        gw = data['gw']
        dv = data['device']

        if not isinstance(ip, str) or not isinstance(nm, int) or not isinstance(gw, str) or not isinstance(dv, str):
            return False
        
        if nm < 0:
            return False
        
        if not self.validate_ip(ip, nm):
            return False
        
        if not self.validate_gw(gw):
            return False
        
        return True

    def validate_put(self, data:dict) -> bool:
        k = ['ip', 'netmaskCIDR', 'gw', 'device']
        c = 0
        
        for a in data.keys():
            if a in k:
                c = c + 1
        
        if c == 0:
            return False
        
        return True
    
    def get(self, id:int):
        if not self.validate_id(id):
            return None, 400

        h = routingDAO.get_rule_from_id(id)
        if h is None:
            return None, 404
        else:
            return h, 200
    
    def post(self, id:int):
        if not self.validate_id(id):
            return None, 400
        
        data = request.json
        if not self.validate_data(data):
            return None, 400
        
        if routingDAO.get_rule_from_id(id) is not None:
            return None, 409
        
        return routingDAO.add_rule_on_id(id, data), 201
        
    def put(self, id:int):
        if not self.validate_id(id):
            return None, 400
        
        data = request.json

        if not self.validate_put(data):
            return None, 400
        
        if routingDAO.get_rule_from_id(id) is None:
            return None, 404
        
        return routingDAO.edit_rule_on_id(id, data), 200
    
    def delete(self, id:int):
        if not self.validate_id(id):
            return None, 400
        
        routingDAO.delete_rule_by_id(id)
        return None, 204

class routingResource(Resource):
    def get(self):
        h = routingDAO.get_table()
        if h is None:
            return None, 404
        else:
            return h, 200
    
    def post(self):
        data = request.json
        h = routingDAO.post_item(data)
        if h is None:
            return None, 404
        else:
            return h, 200

class cleanResource(Resource):
    def post(self):
        routingDAO.clean_db()
        return None, 200