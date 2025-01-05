# Google functions
The functions feature basically allows us to define a function (in our case Python) that is executed in response to a trigger such as PubSub or HTTP hook, our function is as follows:

```python
def my_function(event_data, context):
    # your code goes here
```
Each function has:
 - `event_data`: payload in form of a dictionary
 - `context`: metadata

> [!WARNING]
> Firestore does not support flask 3.0 we will work with Flask 2.3.3

Our `requirements.txt` will look like this:
```text
flask==2.3.3
google-cloud-firestore
numpy
```

In 






## HTTP trigger function (unauthenticated)
*Linux*
```bash
gcloud functions deploy ${FUNCTION_NAME}   --runtime ${RUNTIME}   --trigger-http --allow-unauthenticated
```
*Windows*
```bash
gcloud functions deploy %FUNCTION_NAME%   --runtime %RUNTIME%  --trigger-http --allow unauthenticated
```
#### Url structure
*Linux*
```bash
https://${REGION-PROJECT_ID}.cloudfunctions.net/${FUNCTION}"
```
*Windows*
```bash
https://%REGION-PROJECT_ID%.cloudfunctions.net/%FUNCTION%"
```
#### CLI invocation
*Linux*
```bash
gcloud functions call ${FUNCTION_NAME}   --data '{"name":"Boba Fett"}'
```
*Windows*
```bash
gcloud functions call %FUNCTION_NAME%   --data '{"name":"Boba Fett"}'
```
## PubSub trigger
*Linux*
```
google.pubsub.${TOPIC}.publish
```
*Windows*
```
google.pubsub.%TOPIC%.publish
```
## Firestore triggers
*Linux*
```bash
projects/${PROJECT_ID}/databases/(default)/documents/collection/{document_wildcard}
```
*Windows*
```
projects/%PROJECT_ID%/databases/(default)/documents/collection/{document_wildcard}
```
The wildcard can be used only on documents

 - `document.create`
 - `document.update`
 - `document.delete`
 - `document.write` (create or update)


Typical deployment command:
*Linux*
```bash
gcloud functions deploy ${FUNCTION_NAME}   --runtime ${RUNTIME}   --trigger-event "${EVENT_TYPE}"--trigger-resource "${DOCUMENT_PATH}"
```
*Windows*
```bash
gcloud functions deploy %FUNCTION_NAME%   --runtime %RUNTIME%   --trigger-event "%EVENT_TYPE%"--trigger-resource "%DOCUMENT_PATH%"
```

### Event structure
Each document contains one or more Value objects
```bash
{
"oldValue": { // Update and Delete operations onlyDocument object with pre-operation document snapshot},
"updateMask": { // Update operations onlyDocumentMask object that lists changed fields.},
"value": {Document object with post-operation document snapshot}
}
```

## Deployment and testing
With this command the deploy our function.
*Linux* 
```bash
export FUNCTION=get_status
gcloud functions deploy ${FUNCTION} --runtime python39--trigger-http –allow-unauthenticated --docker-registry=artifact-registry --no-gen2
```

*Windows*
```bash
set FUNCTION=get_status
gcloud functions deploy %FUNCTION% --runtime python39--trigger-http –allow-unauthenticated --docker-registry=artifact-registry --no-gen2
```

### CLI testing
*Linux*
```bash
gcloud functions call ${FUNCTION}
```
*Windows*
```bash
gcloud functions call %FUNCTION%
```
### HTTP request
*Linux*
```bash
export URL=$(gcloud functions describe $FUNCTION | grep url: |awk '{print $2}')
curl -m 70 -X POST  $URL -H "Authorization: bearer $(gcloud auth print-identity-token)"
```
*Windows*
```bash
FOR /F "tokens=2 delims=: " %i IN ('gcloud functions describe %FUNCTION% ^| findstr "url:"') DO SET URL=%i
SET URL=%URL: =%
FOR /F "delims=" %i IN ('gcloud auth print-identity-token') DO SET TOKEN=%i
curl -m 70 -X POST %URL% -H "Authorization: bearer %TOKEN%"
```


