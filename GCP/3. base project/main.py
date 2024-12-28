from flask import Flask, render_template_string,render_template, request
from dao_gcp import DAO
from myForm import MyForm

app = Flask(__name__, static_url_path='/static', static_folder='static') ## instanzia oggetto Flask

dao = DAO()

## dictionary to object
class Struct:
    def __init__(self,**entries):
        self.__dict__.update(entries)




##### Item list route
@app.route('/items', methods=['GET'])
def get_items():
    items = dao.get_items_with_identifier()
    if items is not None:
        return render_template('itemlist.html', items=items)
    else:
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



    
##### Index page of the web app
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', item=None)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',path=request.path),404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080,debug=True)