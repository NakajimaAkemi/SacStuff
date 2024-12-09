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
## Setting up topics 
*Linux*
```bash
export TOPIC=cpu_temperature
gcloud pubsub topics create ${TOPIC}
```
*Windows*
```bash
set TOPIC=cpu_temperature
gcloud pubsub topics create %TOPIC%
```

```
gcloud pubsub topics list
gcloud pubsub topics describe ${TOPIC}
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
