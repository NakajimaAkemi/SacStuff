# Deploying Flask app with Firestore DB
In this exercise we will setup a Flask Application backed by a Firestore DB.

## Firestrore DB
Firestore DB is a schema less Database which can store different documents within the same collections, where Each document is uniquely identified by a name. In our Flask application we need to include **google-cloud-firestore** library.

### Setting up the credentials
*Linux*
```bash
export NAME=webuser
export PROJECT_ID=rlfirestore2024
gcloud iam service-accounts create ${NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com"--role "roles/owner"touch credentials.json
gcloud iam service-accounts keys create credentials.json --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```
*Windows*
```bash
set NAME=webuser
set PROJECT_ID=rlfirestore2024
gcloud iam service-accounts create ${NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com"--role "roles/owner"touch credentials.json
gcloud iam service-accounts keys create credentials.json --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```

### DAO
