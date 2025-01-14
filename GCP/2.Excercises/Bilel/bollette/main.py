from flask import Flask, render_template_string,render_template, request
from flask_restful import Resource, Api
from dao_gcp import DAO
from myForm import MyForm
import json
from datetime import datetime

app = Flask(__name__, static_url_path='/static', static_folder='static') ## instanzia oggetto Flask
dao = DAO()
project_id='socialbilli'
basePath = '/api/v1'
api = Api(app)

############################# USEFUL FUNCTIONS ##############################
## dictionary to object
class Struct:
    def __init__(self,**entries):
        self.__dict__.update(entries)
    
################### API ########################################

class ConsumiResource(Resource):
    def validate_itemdata(self,itemdata):
        for k in ['value']:
             if k not in itemdata.keys():
                return False
        if not isinstance(itemdata['value'],(int)):
                return False
        ## check if number is not negative etc...
        if itemdata['value'] < 0: 
            return False 
        return True
    
    def date_from_str(self,d):
            try: return datetime.strptime(d,'%d-%m-%Y')
            except: return None    
            
    def get(self,data):
        if self.date_from_str(data) is None:
            return None,400
        item = dao.get_lettura_interpolation(data)
        if item is None:
            return None, 404
        else:
            return item, 200

    def post(self,data):
        if self.date_from_str(data) is None:
            return None,400
        itemdata=request.json
        if not self.validate_itemdata(itemdata):
            return None, 400
        item = dao.get_lettura(data) 
        if item is not None: ## Already exists
            return None,409
        dao.add_lettura(data,itemdata['value'])
        item = dao.get_lettura(data)
        return item, 201  
    
    
## Done and tested
class CleanResource(Resource):
    def post(self):
        dao.clean_db()
        return None, 200
    
    def get(self):
        dao.clean_db()
        return None,200
    
api.add_resource(ConsumiResource, f'{basePath}/consumi/<data>')
api.add_resource(CleanResource, f'{basePath}/clean')       
#################################################################################
    



####################### WEB-APP #################################################



##### Item list route
@app.route('/bollette', methods=['GET'])
def get_items():
    items = dao.get_last_bollette()
    if items is not None:
        return render_template('itemlist.html', items=items)
    else:
        return render_template('itemlist.html', items=[])


##### Item route GET
@app.route('/bolletta/<iditem>', methods=['GET'])
def get_item(iditem):
    item = dao.get_bolletta(iditem)
    if item is not None:
        return render_template('item.html', item=item)
    else:
        return render_template('item.html', item=None)



    
##### Index page of the web app
@app.route('/', methods=['GET'])
def index():
    routes = ['bollette']
    return render_template('index.html', routes=routes)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',path=request.path),404
##################################################################################################




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080,debug=True)
