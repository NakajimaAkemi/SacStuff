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
### Creating the project
*Linux*
```bash
export NAME=webuser
export PROJECT_ID=pubsubsac
```
```bash
gcloud projects create ${PROJECT_ID} --set-as-default
gcloud projects describe ${PROJECT_ID}
```
*Windows Shell*
```bash
set NAME=webuser
set PROJECT_ID=pubsubsac
```
```bash
gcloud projects create %PROJECT_ID% --set-as-default
gcloud projects describe %PROJECT_ID%
```
After creating the project we must go to the GCP dashboard and abilitate the `Firestore DB` in native mode (make sure to setup everything in the same region) and the `Cloud Build API` for our project.

### Setting up the credetials
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
