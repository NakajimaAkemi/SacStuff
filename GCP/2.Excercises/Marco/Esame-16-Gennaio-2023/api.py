from flask import request
from flask_restful import Resource
from typing import Optional
from dao import bolletteDao
from utils import date_from_str

dao = bolletteDao()

class consumiDataResource(Resource):

    def validate_data(self, data:str) -> bool:
        if date_from_str(data) is None:
            return False

        return True
    
    def validate_body(self, lettura:dict) -> bool:
        if 'value' not in lettura.keys():
            return False
        
        if not isinstance(lettura['value'], int):
            return False
        
        if lettura['value'] < 0:
            return False
        return True
        
    def get(self, data:str) -> tuple[Optional[dict], int]:
        if not self.validate_data(data):
            return None, 400
        
        h = dao.get_lettura_by_id(data)

        return h, 200
    
    def post(self, data:str) -> tuple[Optional[dict], int]:
        if not self.validate_data(data):
            return None, 400
        
        lettura = request.json

        if not self.validate_body(lettura):
            return None, 400
        
        p = dao.check_if_in(data)

        if p is not None:
            if not p['isInterpolated']:
                return None, 409
            
        h = dao.add_item_by_id(data, lettura)
        return h, 201


    


class cleanResource(Resource):
    def post(self):
        dao.clean_db()
        return None, 200
