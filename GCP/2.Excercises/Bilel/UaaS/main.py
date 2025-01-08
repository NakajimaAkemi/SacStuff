from flask import Flask, render_template_string,render_template, request
from dao_gcp import DAO
from myForm import MyForm, CantiereForm
import json
import os
from google.cloud import pubsub_v1


app = Flask(__name__, static_url_path='/static', static_folder='static') ## instanzia oggetto Flask

dao = DAO()

topic_name='NUOVO-CANTIERE'
project_id='umarellasservice'
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

'''topic_name=os.environ['TOPIC'] if 'TOPIC' in os.environ.keys() else 'NUOVO-CANTIERE'
project_id=os.environ['PROJECT_ID'] if 'PROJECT_ID' in os.environ.keys()  else 'progettinoprovinosecondo'

publisher = pubsub_v1.PublisherClient()'''
'''topic_path = publisher.topic_path(project_id, topic_name)'''


'''
def my_function(event_data,context):
    return "Hello world!"

## dictionary to object
class Struct:
    def __init__(self,**entries):
        self.__dict__.update(entries)

##### Item list route
@app.route('/publish', methods=['GET'])
def get_items():
    items = dao.get_items_with_identifier()
    if items is not None:
        publisher.publish(topic_path, json.dumps("Testing message").encode('utf-8'))
        return render_template('index.html')
    else:
        return render_template('index.html')


##### Item list route
@app.route('/items', methods=['GET'])
def get_items():
    items = dao.get_items_with_identifier()
    if items is not None:
        #publisher.publish(topic_path, json.dumps("STO GUARDANDO LA LISTA DI PERSONE").encode('utf-8'))
        #publisher.publish(topic_path, json.dumps("STO GUARDANDO LE"))
        return render_template('itemlist.html', items=items)
    else:
        publisher.publish(topic_path, json.dumps("STO GUARDANDO LE").encode('utf-8'))
        return render_template('itemlist.html', items=[])


##### Item route GET
#@app.route('/item/<iditem>', methods=['GET'])
#def get_item(iditem):
#    item = dao.get_umarell(iditem)
#    if item is not None:
#        return render_template('item.html', item=item)
#    else:
#        return render_template('item.html', item=None)



#### Item route with form for updates

@app.route("/item/<iditem>", methods=['GET', 'POST'])
def get_item(iditem):
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


<a>Lista di umarells</a>
<ul>
    {%for item in umarells%}
    {% for key, value in item.items() %}
        <li>
            <strong>{{ key }}:</strong>
            {% if value is mapping %}
                <ul>
                    {% for sub_key, sub_value in value.items() %}
                        <li>{{ sub_key }}: {{ sub_value }}</li>
                    {% endfor %}
                </ul>
            {% elif value is iterable and value is not string %}
                <ul>
                    {% for item in value %}
                        <li>{{ item }}</li>
                    {% endfor %}
                </ul>
            {% else %}
                {{ value }}
            {% endif %}
        </li>
    {% endfor %}
    {% endfor %}
</ul>'''
##### Index page of the web app
@app.route('/search', methods=['GET','POST'])
def search():
    cantieri=[]
    umarells=[]
    if request.method == 'POST':
        cform = MyForm(request.form)
        cap = cform.cap.data
        umarell = cform.umarell.data
        cantiere = cform.cantiere.data
        both = cform.both.data
        umarells,cantieri = dao.query(cap,umarell,cantiere,both)
        print(umarells)
        print(cantieri)
        ### post
        

    cform = MyForm()
    return render_template('item_form.html', form=cform,cantieri=cantieri,umarells=umarells)

@app.route('/addCantiere', methods=['GET','POST'])
def add_cantiere():
    if request.method == 'POST':
        cform = CantiereForm(request.form)
        cap = cform.cap.data
        id = cform.id.data
        indirizzo = cform.indirizzo.data
        dao.add_cantiere(id,indirizzo,cap)
        if dao.get_cantiere(id) is not None:
           publisher.publish(topic_path, json.dumps("Nuovo cantiere " + str(indirizzo) + "CAP: "+str(cap)).encode('utf-8'))
        ### post
        

    cform = CantiereForm()
    return render_template('cantiere_form.html', form=cform)

    
    
##### Index page of the web app
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', item=None)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',path=request.path),404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080,debug=True)