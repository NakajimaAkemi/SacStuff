# Google functions
The functions are executed in response of a trigger which can be in many forms such as PubSub or event HTTPS, each Event has Event Data and Context object.

```text
flask==2.3.3
google-cloud-firestore
numpy
```
> [!WARNING]
> Firestore does not support flask 3.0
def my_function(event_data, context) where:
 - `event_data` is the payload in form of a dictionary
 - `context` is the metadata

## HTTP trigger function (unauthenticated)
```
gcloud functions deploy ${FUNCTION_NAME}   --runtime ${RUNTIME}   --trigger-http --allow-unauthenticated
```
#### Url structure
```
https://${REGION-PROJECT_ID}.cloudfunctions.net/${FUNCTION}"
```
#### Cli invocation
```
gcloud functions call ${FUNCTION_NAME}   --data '{"name":"Boba Fett"}'
```
## PubSub trigger
```
google.pubsub.${TOPIC}.publish
```
## Firestore triggers
```
projects/${PROJECT_ID}/databases/(default)/documents/collection/{document_wildcard}
```
The wildcard can be used only on documents

 - `document.create`
 - `document.update`
 - `document.delete`
 - `document.write` (create or update)


Typical deployment command:
```bash
gcloud functions deploy ${FUNCTION_NAME}   --runtime ${RUNTIME}   --trigger-event "${EVENT_TYPE}"--trigger-resource "${DOCUMENT_PATH}"
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
```bash


