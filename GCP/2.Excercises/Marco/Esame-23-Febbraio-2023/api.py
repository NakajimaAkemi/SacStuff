from flask import Flask, request
from flask_restful import Resource, Api
from typing import Optional
from dao import chirpsDAO

dao = chirpsDAO()

class chirpsResource(Resource):
    def validate_body(self, msg:Optional[str]):
        if not isinstance(msg, str):
            return False
        
        if len(msg) == 0:
            return False
        
        return True
        
    def post(self) -> tuple[Optional[dict], int]:
        data = request.json
        if not self.validate_body(data):
            return None, 400
        
        h = dao.add_new_chirp(data)
        if h is None:
            return None, 400
        else:
            return h, 200
    
class chirpsIdResource(Resource):

    def get(self, id:str) -> tuple[Optional[dict], int]:
        h = dao.get_chirp_by_id(id)
        if h is None:
            return None, 404
        else:
            return h, 200

class cleanResource(Resource):
    
    def post(self) -> None:
        dao.clean_db()
        return None, 200
    
    def get(self) -> None:
        dao.clean_db()
        return None,200