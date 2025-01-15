from flask import Flask, request, render_template
from flask_restful import Api 
import requests
import json
from api import chirpsResource, chirpsIdResource, cleanResource
from form import messageForm, hashtagForm
from publisher import send_message
from utils import get_hashtags
from dao import chirpsDAO

app = Flask(__name__,
    static_folder='static',
    static_url_path='/static'
)

dao = chirpsDAO()
@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html'), 200

@app.route('/chirps', methods=['GET', 'POST'])
def chirp():
    posted = False
    if request.method == 'POST':
        cform1 = messageForm(request.form)
        message = cform1.message.data

        r = requests.post('https://uaas070120252.nw.r.appspot.com/api/v1/chirps', json=message)

        if r.status_code == 200:
            posted = True
            hashtags = get_hashtags(message)
            for h in hashtags:
                send_message(h, message)
        else:
            posted = False
    
    cform1 = messageForm()
    cform2 = hashtagForm()
    return render_template('chirps.html', form1 = cform1, form2 = cform2, posted = posted)

@app.route('/search_hashtag', methods = ['POST'])
def chirp_tags():
    cform = hashtagForm(request.form)
    hashtag = cform.hashtag.data
    messages = dao.get_hashtag(hashtag)
    
    return render_template('chirp_tags.html', hashtag=hashtag, messages = messages)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',path=request.path),404

api = Api(app)
base_url = '/api/v1'

api.add_resource(chirpsResource, f'{base_url}/chirps')
api.add_resource(chirpsIdResource, f'{base_url}/chirps/<string:id>')
api.add_resource(cleanResource, f'{base_url}/clean')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
