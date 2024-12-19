# Google functions
The functions are executed in response of a trigger which can be in many forms such as PubSub or event HTTPS. Each Event has Event Data and Context object


def my_function(event_data, context) where:
 - event_data is the payload in form of a dictionary
 - context is the metadata

## HTTP trigger function (unauthenticated)
gcloud functions deploy ${FUNCTION_NAME}   --runtime ${RUNTIME}   --trigger-http --allow-unauthenticated
Url structure
https://${REGION-PROJECT_ID}.cloudfunctions.net/${FUNCTION}"

Cli invocation
gcloud functions call ${FUNCTION_NAME}   --data '{"name":"Boba Fett"}'
## PubSub trigger
google.pubsub.${TOPIC}.publish

## Firestore triggers

projects/${PROJECT_ID}/databases/(default)/documents/collection/{document_wildcard}
The wildcard can be used only on documents

document.create
document.update
document.delete
document.write create or update



