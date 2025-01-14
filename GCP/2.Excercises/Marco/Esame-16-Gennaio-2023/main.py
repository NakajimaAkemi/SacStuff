from flask import Flask, request, render_template
from flask_restful import Api 
from api import consumiDataResource, cleanResource
from dao import bolletteDao

app = Flask(__name__,
    static_folder='static',
    static_url_path='/static'
)
api = Api(app)
base_url = '/api/v1'

dao = bolletteDao()
@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/bollette', methods = ['GET'])
def bollette_page():
    bollette_l = dao.get_last_year_billings()
    print(bollette_l)
    return render_template('list_bollette.html', bollette_l=bollette_l)


api.add_resource(consumiDataResource, f'{base_url}/consumi/<string:data>')
api.add_resource(cleanResource, f'{base_url}/clean')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
