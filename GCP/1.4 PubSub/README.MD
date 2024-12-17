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
```python
#!/usr/bin/python3
import timefrom datetime 
import datetimeimport json
import os
from google.cloud import pubsub_v1
update_interval=5.0
topic=os.environ['TOPIC'] if os.environ['TOPIC'] else 'cpu_temperature'
project_id=os.environ['PROJECT_ID'] if os.environ['TOPIC'] else 'myprj'
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic)
print(topic_path)

def get_cpu_temp():
  with open("/sys/class/thermal/thermal_zone0/temp") as f:
    return float(f.read())/ 1000 
def notify_cpu_temp(temp):
    now = datetime.now()
    data={'timestamp': now.timestamp(), 'time': str(now), 'temperature': temp}
    res = publisher.publish(topic_path, json.dumps(data).encode('utf-8'))
    print(data, res.result())
if __name__=='__main__':
    while True:
          notify_cpu_temp(get_cpu_temp())
          time.sleep(update_interval)
```

### Subscriber script ingestion.py
```python
#!/usr/bin/python3
import os
import json
from google.cloud import pubsub_v1
subscription_name=os.environ['SUBSCRIPTION_NAME'] if os.environ['SUBSCRIPTION_NAME'] else 'cpu_temperature'
project_id=os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'myprj'
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)
if __name__=='__main__':
      pull = subscriber.subscribe(subscription_path, callback=callback)
      try:
          pull.result(timeout=30)
      except:
          pull.cancel()
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
