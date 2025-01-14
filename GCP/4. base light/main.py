from flask import Flask, render_template_string,render_template, request
from flask_restful import Resource, Api
from dao_gcp import DAO
from myForm import MyForm
import json
from google.cloud import pubsub_v1

app = Flask(__name__, static_url_path='/static', static_folder='static') ## instanzia oggetto Flask
dao = DAO()
project_id='sacbilelarfaoui'
publisher = pubsub_v1.PublisherClient()
basePath = '/api/v1'
api = Api(app)

############################# USEFUL FUNCTIONS ##############################
## dictionary to object
class Struct:
    def __init__(self,**entries):
        self.__dict__.update(entries)


##############################  PUBLISH #####################################
def check_topic_exists(topic_path):    
    try:
        publisher.get_topic(request={"topic": topic_path})
        print("Topic exists.")
        return True
    except:
        print("Topic does not exist.")
        return False


def send_message(my_topic,message):
    #my_topic = topic.replace("#","")
    topic_path = publisher.topic_path(project_id, my_topic)
    if not check_topic_exists(topic_path):
        publisher.create_topic(request={"name": topic_path})
        print(f"Created topic: {my_topic}")
    publisher.publish(topic_path, json.dumps(message).encode('utf-8'))
    
################### API ########################################

class ItemResource(Resource):
    def validate_itemdata(self,itemdata):
        for k in ['property1','property2','...']:
             if k not in itemdata.keys():
                return False
        if not isinstance(itemdata['propertyint'],(int)) or not isinstance(itemdata['propertystr'],(str)):
                return False
        ## check if number is not negative etc...
        return True
    
    ### se non forziamo int nel path
    def validate_id(self,id):
        try:
            int_value = int(id)
            return int_value >= 0
        except:
            print(str(id)+" non rappresenta un intero")
            return False
        
    def validate_update(self,item,itemdata):
        valid_keys = ['ip', 'netmaskCIDR', 'gw', 'device']
        if not set(itemdata.keys()).issubset(valid_keys):
            return False
        item_to_check=item 
        item_to_check.update(itemdata)
        if not isinstance(item_to_check['ip'],str) or not isinstance(item_to_check['netmaskCIDR'], int) or not isinstance(item_to_check['gw'], str) or not isinstance(item_to_check['device'], str):
            return False 
        elif not self.is_valid_ipv4(item_to_check['ip']) or not self.is_ip_valid_with_netmask(item_to_check['ip'], item_to_check['netmaskCIDR']):
                return False
        return True  
    
    def get(self,iditem):
        item = dao.get_item(iditem)
        if item is None:
            return None, 404
        else:
            return item, 200

    def post(self,iditem):
        itemdata=request.json
        if not self.validate_itemdata(itemdata):
            return None, 400
        item = dao.get_item(iditem) 
        if item is not None: ## Already exists
            #return item, 409
            return None,409
        dao.add_item(iditem,itemdata['property1'],itemdata['property2'])
        item = dao.get_item(iditem)
        return item, 201  
    '''
    def delete(self,iditem):
        if not self.validate_id(iditem):
            return None, 400
        item = dao.get_rule(iditem) 
        if item is None: ## Does not exist
            return item, 404
        dao.delete_rule(iditem)
        #item = dao.get_item(iditem)
        return None, 204
        #return None, 200
        
    def put(self,iditem): ### tested (see what responses the validator wants)
        if not self.validate_id(iditem):
            return None, 400
        itemdata=request.json
        item = dao.get_rule(iditem)
        if item is None :
            return None,404
        
        if not self.validate_update(item,itemdata):
            return None, 400
        
        dao.update_rule(iditem,itemdata)
        item = dao.get_rule(iditem)
        return item, 200  '''
    
    
    
## Done and tested
class CleanResource(Resource):
    def post(self):
        dao.clean_db()
        return None, 200
    
    def get(self):
        dao.clean_db()
        return None,200
    
api.add_resource(ItemResource, f'{basePath}/item/<int:iditem>')
api.add_resource(CleanResource, f'{basePath}/clean')       
#################################################################################
    



####################### WEB-APP #################################################



##### Item list route
@app.route('/items', methods=['GET'])
def get_items():
    #items = dao.get_items_with_identifier()
    items = None
    if items is not None:
        return render_template('itemlist.html', items=items)
    else:
        #publisher.publish(topic_path, json.dumps("STO GUARDANDO LE").encode('utf-8'))
        return render_template('itemlist.html', items=[])


##### Item route GET
@app.route('/item/<iditem>', methods=['GET'])
def get_item(iditem):
    #item = dao.get_umarell(iditem)
    item = None
    if item is not None:
        return render_template('item.html', item=item)
    else:
        return render_template('item.html', item=None)



#### Item route with form for updates
@app.route("/item_form/<iditem>", methods=['GET', 'POST'])
def get_item_form(iditem):
    c = dao.get_item(iditem)
    if request.method == 'POST':
        cform = MyForm(request.form)
        if c:
            # Insert if not present already
            dao.update_item(iditem, cform.nome.data, cform.cognome.data, cform.cap.data)
            c = dao.get_item(iditem)
        else:
            # If item exists we will update it
            dao.add_item(iditem, cform.nome.data, cform.cognome.data, cform.cap.data)
            c = dao.get_item(iditem)
    
    # GET: recupera il form con i dati del colore
    if c is None:
        c = { 'propert1': "value", 'property2': "value",'...':0}

    cform = MyForm(obj=Struct(**c))
    
    return render_template(
        'item_form.html',
        item=c,
        form=cform
    )



    
##### Index page of the web app
@app.route('/', methods=['GET'])
def index():
    routes = ['','']
    return render_template('index.html', routes=routes)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',path=request.path),404
##################################################################################################




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080,debug=True)
