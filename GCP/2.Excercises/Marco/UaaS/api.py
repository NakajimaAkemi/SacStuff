from flask import Flask, request
from flask_restful import Resource, Api
from uaas_dao import Uaas
from typing import Optional

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static'
            )

api = Api(app)
uaas_dao = Uaas()
base_url = '/api/v1'

class Umarell(Resource):
    def validate_umarell(self, data:dict) -> bool:
        for k in ['nome', 'cognome', 'cap']:
            if k not in data.keys():
                return False
        
        if not isinstance(data['nome'], str) or not isinstance(data['cognome'], str) or not isinstance(data['cap'], int):
            return False

        return True
    
    def get(self, idumarell:int) -> Optional[dict]:
        c = uaas_dao.get_umarell_by_id(idumarell)
        if c is None:
            return None, 404
        else:
            return c, 200
    
    def post(self, idumarell:dict) -> Optional[dict]:
        data = request.json
        if not self.validate_umarell(data):
            return None, 400
        if uaas_dao.get_umarell_by_id(idumarell) is not None:
            return None, 409
        
        uaas_dao.add_umarell(idumarell, data['nome'], data['cognome'], data['cap'])
        return data, 201
    
class Cantiere(Resource):
    def validate_cantiere(self, data:dict) -> bool:
        for k in ['indirizzo', 'cap']:
            if k not in data.keys():
                return False

        if not isinstance(data['indirizzo'], str) or not isinstance(data['cap'], int):
            return False
        
        return True
    
    def get(self, idcantiere:int) -> Optional[dict]:
        c = uaas_dao.get_cantiere_by_id(idcantiere)
        if c is None:
            return None, 404
        else:
            return c, 200
    
    def post(self, idcantiere):
        data = request.json
        if not self.validate_cantiere(data):
            return None, 400
        if uaas_dao.get_cantiere_by_id(idcantiere) is not None:
            return None, 409
        
        uaas_dao.add_cantiere(idcantiere, data['indirizzo'], data['cap'])
        
        return data, 201
        
class Clean(Resource):
    def get(self):
        uaas_dao.clear_db()
        return None, 200

api.add_resource(Umarell, f'{base_url}/umarell/<int:idumarell>')
api.add_resource(Cantiere, f'{base_url}/cantiere/<int:idcantiere>')
api.add_resource(Clean, f'{base_url}/clean')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)