# PubSub
Our `requirements.txt` should look like this.
```Python
flask
requests
google-cloud-firestore
google-cloud-pubsub
numpy
gunicorn
```
## Creating the project and credentials setup
*Linux*
```bash
export NAME=pubsubuser
export PROJECT_ID=pubsubsac
```
*Windows Shell*
```bash
set NAME=pubsubuser
set PROJECT_ID=pubsubsac
```
Then we create our project.
```bash
gcloud projects create %PROJECT_ID% --set-as-default
gcloud projects describe %PROJECT_ID%
```
> [!IMPORTANT]
> We need to abilitate the FirestoreDB, Cloud Build API and  PubSub on the dashboard.

### Setting up the credetials
This process is no different than the one we setup with FirestoreDB.
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
## Setting up pub sub
### Creating topics
*Linux*
```bash
export TOPIC=cpu_temperature
gcloud pubsub topics create ${TOPIC}
```
```
gcloud pubsub topics list
gcloud pubsub topics describe ${TOPIC}
```
*Windows*
```bash
set TOPIC=cpu_temperature
gcloud pubsub topics create %TOPIC%
```
```
gcloud pubsub topics list
gcloud pubsub topics describe %TOPIC%
```

### Subscription 
*Linux*
```bash
export SUBSCRIPTION_NAME=cpu_sub
gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME} --topic ${TOPIC}
```
*Windows*
```bash
set SUBSCRIPTION_NAME=cpu_sub
gcloud pubsub subscriptions create %SUBSCRIPTION_NAME% --topic %TOPIC%
```

### Message 
#### Sending
*Linux*
```bash
gcloud pubsub topics publish  ${TOPIC} --attribute=from="cli" --message="Test Message"
```
*Windows*
```bash
gcloud pubsub topics publish  %TOPIC% --attribute=from="cli" --message="Test Message"
```
#### Pulling
*Linux*
```bash
gcloud pubsub subscriptions pull ${SUBSCRIPTION_NAME}
```
*Windows*
```bash
gcloud pubsub subscriptions pull %SUBSCRIPTION_NAME%
```
### Publisher script publisher.py
In the repository we can find the `publisher.py` script which fetches the env variables and then send data to the topic with the call `publisher.publish(topic, data)`.

### Subscriber script ingestion.py
The other script `ingestion.py` will listen to the topic with a timeout and saves everything in the firestore.


## Publish and subscribe token based
We create another topic and then set it up with HTTPS webhook and it will the default service for app engine.

*Linux*
```bash
export TOPIC2=cpu_temperature_alert
gcloud pubsub topics create ${TOPIC2}
gcloud pubsub topics describe ${TOPIC2}
export TOKEN="123token"
export SUBSCRIPTION_NAME2="cpu_alert_sub"
gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME2} --topic ${TOPIC2} --push-endpoint   
 "https://${PROJECT_ID}.appspot.com/pubsub/push?token=${TOKEN}" --ack-deadline 10
```

*Windows*
```bash
set TOPIC2=cpu_temperature_alert
gcloud pubsub topics create %TOPIC2%
gcloud pubsub topics describe %TOPIC2%
set TOKEN="123token"
set SUBSCRIPTION_NAME2="cpu_alert_sub"
gcloud pubsub subscriptions create %SUBSCRIPTION_NAME2% --topic %TOPIC2% --push-endpoint   
 "https://%PROJECT_ID%.appspot.com/pubsub/push?token=%TOKEN%" --ack-deadline 10
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
