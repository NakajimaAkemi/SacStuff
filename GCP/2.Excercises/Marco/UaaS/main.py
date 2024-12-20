from flask import Flask, request, render_template
from uaas_dao import Uaas

app = Flask(__name__,
    static_folder='static',
    static_url_path='/static'
)

uaas_dao = Uaas()

@app.route("/", methods=["GET"])
def homepage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)