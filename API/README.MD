# Restful API
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
Is based on Swagger specification
