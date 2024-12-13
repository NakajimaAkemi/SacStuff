from flask import Flask, render_template_string,render_template, request

#template='''<html><body><h1>Hello {{recipient}}</h1></body></html>
#'''

app = Flask(__name__, static_url_path='/static', static_folder='static') ## instanzia oggetto Flask

@app.route("/<recipient>", methods=['GET'])
def hello(recipient):
    return render_template('hello.html',recipient=recipient)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',path=request.path),404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080,debug=True)
