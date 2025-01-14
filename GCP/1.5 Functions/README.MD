# Google functions
The functions feature basically allows us to define a function (in our case Python) that is executed in response to a trigger such as PubSub or HTTP hook, our function is as follows:

```python
def my_function(event_data, context):
    # your code goes here
```
Each function has:
 - `event_data`: payload in form of a dictionary
 - `context`: metadata

Or for the http triggered event.
```python
def my_function(request):
    # your code goes here
```



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
export FUNCTION_NAME=my_function
export RUNTIME=python39
```
*Windows*
```bash
set FUNCTION_NAME=my_function
set RUNTIME=python39
```


## HTTP trigger function (unauthenticated)
*Linux*
```bash
gcloud functions deploy ${FUNCTION_NAME}   --runtime ${RUNTIME}   --trigger-http --allow-unauthenticated --docker-registry=artifact-registry --no-gen2 --region europe-west2
```
*Windows*
```bash
gcloud functions deploy %FUNCTION_NAME%   --runtime %RUNTIME%  --trigger-http --allow-unauthenticated --docker-registry=artifact-registry --no-gen2 --region europe-west2
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
Should be an event type, i dunno.

*Linux*
```bash
gcloud functions deploy ${FUNCTION_NAME} --runtime ${RUNTIME} --trigger-topic ${TOPIC} --docker-registry=artifact-registry --no-gen2 --region europe-west2
```
*Windows*
```
gcloud functions deploy %FUNCTION_NAME% --runtime %RUNTIME% --trigger-topic %TOPIC% --docker-registry=artifact-registry --no-gen2 --region europe-west2
```
## Firestore triggers
We can trigger a function with an action over a firestore document, we need define the 
*Linux*
```bash
export EVENT_TYPE=providers/cloud.firestore/eventTypes/action_wildcard
export DOCUMENT_PATH="projects/${PROJECT_ID}/databases/(default)/documents/collection/{document_wildcard}"
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
gcloud functions deploy ${FUNCTION_NAME} --runtime=${RUNTIME} --trigger-event=${EVENT_TYPE} --trigger-resource?${DOCUMENT_PATH} --docker-registry=artifact-registry --no-gen2 --region europe-west2
```
*Windows*
```bash
gcloud functions deploy %FUNCTION_NAME%   --runtime %RUNTIME%   --trigger-event "%EVENT_TYPE%" --trigger-resource "%DOCUMENT_PATH%" --docker-registry=artifact-registry --no-gen2 --region europe-west2
```

The data is structured as the following:
```python
{
    "oldValue": { // Update and Delete operations only
        A Document object containing a pre-operation document snapshot
    },
    "updateMask": { // Update operations only
        A DocumentMask object that lists changed fields.
    },
    "value": {
        // A Document object containing a post-operation document snapshot
    }
}
```

