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

## ENV Variables to setup
These variables are needed to setup our functions.
*Linux*
```bash
export FUNCTION=my_function
export RUNTIME=python39
```
*Windows*
```bash
set FUNCTION=my_function
set RUNTIME=python39
```


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
The url is structured as follows:
 - `REGION`: where we deployed the project
 - `PROJECT_ID`
 - `FUNCTION`

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
We can trigger a function with an action over a firestore document, we need define the 
*Linux*
```bash
expose EVENT_TYPE = providers/cloud.firestore/eventTypes/action_wildcard
expose DOCUMENT_PATH = projects/%PROJECT_ID%/databases/(default)/documents/collection/{document_wildcard}
```
*Windows*
```bash
set EVENT_TYPE = providers/cloud.firestore/eventTypes/action_wildcard
set DOCUMENT_PATH = projects/%PROJECT_ID%/databases/(default)/documents/collection/{document_wildcard}
```
The action wildcard can be:
 - `document.create`
 - `document.update`
 - `document.delete`
 - `document.write` (create or update)


Typical deployment command:
*Linux*
```bash
gcloud functions deploy ${FUNCTION_NAME}   --runtime ${RUNTIME}   --trigger-event "${EVENT_TYPE}" --trigger-resource "${DOCUMENT_PATH}" --docker-registry=artifact-registry --no-gen2 
```
*Windows*
```bash
gcloud functions deploy %FUNCTION_NAME%   --runtime %RUNTIME%   --trigger-event "%EVENT_TYPE%" --trigger-resource "%DOCUMENT_PATH%" --docker-registry=artifact-registry --no-gen2
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
gcloud functions deploy %FUNCTION% --runtime python39 --trigger-http –allow-unauthenticated --docker-registry=artifact-registry --no-gen2
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


