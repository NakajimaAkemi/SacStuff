# Colors application
In this section we will create a web application that manages the RGB values of colors, including a Firestore Databases, Forms for editing and API documentation with Swagger. We define a Color DAO which is has the same structure as the former example that allows CRUD operations.

## WTForms
In order to manage and validate the form field we include the WTForms library, which allows us to define a form object and define each field as its properties.  In our case we are trying to bind our form to the Color DAO object.
```Python
from wtforms import Form, IntegerField,validators
class ColorForm(Form):
    red = IntegerField('Red', [validators.NumberRange(min=0,max=255)])
    green = IntegerField('Green', [validators.NumberRange(min=0,max=255)])
    blue = IntegerField('Blue', [validators.NumberRange(min=0,max=255)])
```
We need to reference them also in the HTML template.
```HTML
<form method="POST">
<table>
    <tr><td>{{form.red.label}}</td><td>{{form.red}}</td></tr>
    <tr><td>{{form.green.label}}</td><td>{{form.green}}</td></tr>
    <tr><td>{{form.blue.label}}</td><td>{{form.blue}}</td></tr>
    <tr><td></td><td><input type="submit" value="Edit"></td></tr>
</table>
</form>
```
In our route `/colors/<color>` we fetch the inputs from the `POST` request.
```Python
cform=Colorform(request.form)
colors_dao.add_color(color, cform.red.data, cform.green.data, cform.blue.data)
```
If the request is `GET` we create a we initialize the form bu using the class Struct.
```Python

## dictionary to object
class Struct:
    def __init__(self,**entries):
        self.__dict__.update(entries)
.....

c=colors_dao.get_color_by_name(color)
cform=Colorform(obj=Struct(**c)))
```

## API setup
First of all we do a recall about HTTP REST:
 - REST is a stateless paradigm
 - Each resource is identified by an URI
 - The types of access are mapped over HTTP methods `POST`,`GET`,`PUT`,`DELETE`...
 - The outcome of the request is defined by a status code
 - The URI path is `/api/version/resource/label/`

### API definition document
We describe our API in a YAML document, where we specify, endpoints, operations, parameters and return values on each operation, authentication methods and more. The first portion of our YAML document specifies the information metadata, base path, host and schemes(protocols).

```yaml
swagger: "2.0"
info:
    title: "Colors"
    description: "Manage color with RGB components"
    version: "1.0.0"
host: "api-dot-colors20221001.appspot.com"
basePath: "/api/v1"
schemes:
    - "https"
```
In the YAML file we will define the different `paths` of our API, specifying the name, rpute, parameters, the allowed action, response codes and data's schema.

```yaml
paths:
    /colors/{colorName}:
        parameters:
      - name: colorName
        in: path
        description: 'Name of the color'
        type: string
        required: true
    get:
      description: "Get color RGB from color name"
      operationId: "colorGet"
      responses:
          200:
              description: "Success."
              schema:
                  $ref: "#/definitions/Color"
          404:
              description: "color not found"
    post:
      description: "add a new Color"
      operationId: "colorPost"
      consumes:
          - application/json
      parameters:
      - in: body
        name: color
        description: "Color object"
        schema:
          $ref: "#/definitions/Color"
        required: true 
      responses:
          204:
              description: "Color added."
          400:
              description: "Invalid color"
          409:
              description: "Already inserted"
```
As last piece of our YAML Api description document we will add the definitions, which specifies the schema of our data. The following data is referenced in the rest of the file with the format `#/definitions/Name`.

```yaml
definitions:
    ColorList:
      type: array
      items:
        type: string
    Color:
      type: object
      properties: 
        red: 
          type: integer
          minimum: 0
          maximum: 255
        green: 
          type: integer
          minimum: 0
          maximum: 255
        blue: 
          type: integer
          minimum: 0
          maximum: 255
```
### API main program
We use in our case the `flask_restful` library in order to setup the API's main program, where we define the API as classes. The first part is including the libraries, deinining the API and the basepath.

```Python
from flask import Flask, request
from flask_restful import Resource, Api
app = Flask(__name__,static_url_path='/static',static_folder='static')
api = Api(app)
colors_dao= Colors()
basePath = '/api/v1'
```
The API works on resouces, we define for example a ColorsResource which allows us to define the HTTP methods functions that return data and the response code according to our API definition, then add it to our API object.

```Python
class ColorsResource(Resource):
    def get(self,colorname):
        colorname=colorname.lower()
        color = colors_dao.get_color_by_name(color_name)
        if color is None:
            return None, 404
        else:
            return color, 200
    def post(self,colorname):
            colordata=request.json()
            print("got POST request: "+str(colordata))
            if not self.validate_colordata(colordata):
                return None, 400
            if colors_dao.get_color_by_name(colorname) is not None:
                return None, 409
            colors_dao.add_color(colorname, colordata['red'],colordata['green'],colordata['blue'])
            return None, 201

api.add_resource(ColorsResource, f'{basePath}/colors/<string:colorname>')
```
We can also validate our form input by fetching the data from the form `request.json`.
```Python
def validate_colordata(self, colordata):
        for k in ['red','green','blue']:
             if k not in colordata.keys():
                return False
             if not isinstance(colordata[k],(int)):
                  return False
             if colordata[k] < 0 or colordata[k]>255:
                return False
        return True
```
### Testing locally
We can test our API locally with this python script.
```Python
#/usr/bin/python3
import requests
base_url='http://localhost:8080/api/v1/colors'
#list colors
r=requests.get(base_url+'/')
print('Available colors: '+ str(r.json()))
# get color
r=requests.get(base_url+'/wisteria')
print('Wisteria color: '+ str(r.json()))
```
### Defining the API's deployment descriptor 
In the GCP project we need to enable the Build API feature
We define the API's deployment descriptor `api.yaml`, we define the entrypoint with `gunicorn`
```yaml
runtime: python39
service: api
entrypoint: gunicorn api:app
handlers:
    - url: /static
      static_dir: static
    - url: /.*
      secure: always
      script: auto
```

## Deploying everything to GCP
After testing our API locally we are ready to deploy everything to GCP.
Our requirements.txt file should look like this.
```text
flask
requests
wtforms
google-cloud-firestore
flask-restful
gunicorn
```
### Creating the project
*Linux*
```bash
export NAME=webuser
export PROJECT_ID=APIcolors08122024
```
```bash
gcloud projects create ${PROJECT_ID} --set-as-default
gcloud projects describe ${PROJECT_ID}
```
*Windows Shell*
```bash
set NAME=webuser
set PROJECT_ID=APIcolors08122024
```
```bash
gcloud projects create %PROJECT_ID% --set-as-default
gcloud projects describe %PROJECT_ID%
```
After creating the project we must go to the GCP dashboard and abilitate the `Firestore DB` in native mode (make sure to setup everything in the same region) and the `Cloud Build API` for our project.


### Setting up the Firestore DB 
*Linux*

```bash
gcloud iam service-accounts create ${NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/owner"
touch credentials.json
gcloud iam service-accounts keys create credentials.json --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```
*Windows*

```bash
gcloud iam service-accounts create %NAME%
gcloud projects add-iam-policy-binding %PROJECT_ID% --member "serviceAccount:%NAME%@%PROJECT_ID%.iam.gserviceaccount.com" --role "roles/owner"
gcloud iam service-accounts keys create credentials.json --iam-account %NAME%@%PROJECT_ID%.iam.gserviceaccount.com
set GOOGLE_APPLICATION_CREDENTIALS=%cd%\credentials.json
```


#### Deploy the app
Classic web app deployment
```bash
gcloud app deploy app.yaml
```

API deploymnet
```bash
gcloud app deploy api.yaml
```







