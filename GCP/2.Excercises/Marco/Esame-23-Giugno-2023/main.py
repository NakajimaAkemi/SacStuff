from flask import Flask, request, render_template
from flask_restful import Api
from api import routingIDResource, routingResource, cleanResource
from dao import routingDAO
from form import ipForm
from utils import ip_validation

app = Flask(__name__,
    static_folder='static',
    static_url_path='/static'
)
api = Api(app)
base_url = '/api/v1'
api.add_resource(routingIDResource, f'{base_url}/routing/<id>')
api.add_resource(routingResource, f'{base_url}/routing')
api.add_resource(cleanResource, f'{base_url}/clean')

@app.route('/', methods=['GET', 'POST'])
def homepage():
    rules = routingDAO.get_table_with_attr()
    found_index = -1
    error_on_ip = False
    error_on_ro = False
    ip = ''
    if request.method == 'POST':
        cform = ipForm(request.form)
        ip = cform.ip.data

        if not ip_validation(ip):
            error_on_ip = True
        else:
            found_index = routingDAO.post_item(ip)
            error_on_ip = False
            if found_index is None:
                found_index = -1
                error_on_ro = True
            else:
                error_on_ro = False
                

    cform = ipForm()
    return render_template(
        'index.html', 
        form=cform, 
        rules=rules, 
        found_index=found_index, 
        error_on_ip=error_on_ip,
        error_on_ro=error_on_ro,
        ip = ip)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',path=request.path),404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
