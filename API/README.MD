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
In our route `/colors/<color>`
```Python
<form method="POST">
<table>
    <tr><td>{{form.red.label}}</td><td>{{form.red}}</td></tr>
    <tr><td>{{form.green.label}}</td><td>{{form.green}}</td></tr>
    <tr><td>{{form.blue.label}}</td><td>{{form.blue}}</td></tr>
    <tr><td></td><td><input type="submit" value="Edit"></td></tr>
</table>
</form>
```


First of all we do a recall about HTTP REST:
 - REST is a stateless paradigm
 - Each resource is identified by an URI
 - The types of access are mapped over HTTP methods 
 - The outcome of the request is defined by a status code
 - The URI path is /api/version/resource/label/

*example*
Color API
/api/v0.1/color/yellow
POST: create a new color given RGB values
Content-type: application/json{‘red’: 255, ‘green’: 255, ‘blue’: 0}
Form data:
Content-type: application/x-www-form-urlencodedred=255&green=255&blue=0
Rest compliant response
400 Bad request{‘message’: ‘invalid request parameters’}
200 OK{‘status’: ‘ko’,‘message’: ‘invalid request parameters’}

/api/v0.1/json/color/yellow
{“red”: 255,“green”: 255,“blue”: 0}

## OpenAPI
Is based on Swagger initiative the API describes:
 - Endpoints
 - Operations on each endpoints (HTTP methods)
 - Parameters and return values on each operation
 - Authetication methods
 - Contact information, license, terms of use, ...

An API can be described by a JSON or YAML document

consumes and produces are the mime types accepted and given in output
base path is the prefix for api
schemes are the accepted protocols
paths is the list of API entrypoints, which defines the method 
parametrers and responses

swagger: "2.0"
info:
 title: Sample API
 description: "API descr."
 version: 1.0.0
host: api.example.com
basePath: /v1
schemes:
 - https
consumes:
 - application/json
 - application/xml
produces:
 - application/json
 - application/xml
paths:
 /users/{userId}:
  get:
    summary: "Get user"
    parameters:
     - in: path
       name: userId
       required: true
       type: integer
       minimum: 1
       Description: "..."
    responses:
       200:
           description: OK
           schema:
               type: object
               properties:
                   id:
                      type: integer
                      example: 4
                   name:
                      type: string
                      example: "RL"
       400:
           description: "..."
definitions:
     User:
       properties:
              id:
                type: integer
              name:
                type: string
        # in response section
schema:
     $ref: '#/definitions/User'


securityDefinitions:BasicAuth:type: basicsecurity:- BasicAuth: []





