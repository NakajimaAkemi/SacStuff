from flask import Flask, render_template, request
#from horses_local import Horses
from horses import Horses
#from horses_gcp import Horses

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static')
horses_dao=Horses()

@app.route('/horse/<horse>', methods=['GET'])
def get_horse(horse):
    ngen=4
    p=horses_dao.get_pedigree(horse, ngen=ngen)
    hrs=horses_dao.get_horse(horse)
    return render_template('pedigree.html', horse=hrs, pedigree=p, nrows=(len(p[ngen-1])))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', path=request.path), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)