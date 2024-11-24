# GCPexercises
In this repo i will put my exercises for the "Sistemi e Applicazioni Cloud" exam @UNIMORE. The prerequisites are having an Google Cloud Platform account(don't use your accademic mail, it may block you from certain features) and having the GCP SDK installed. This repository's main theme is about deploying a Flask web application to the GCP.

## CLI commands
Make sure to have the gcloud components up to date and check for the python engine support.
```bash
gcloud components update
gcloud components install app-engine-python
```

### Login 
```bash
gcloud auth login
```

### Project creation
#### Bash
```bash
export PROJECT_ID=<your-project-name>
gcloud projects create ${PROJECT_ID} --set-as-default
```
#### Windows Shell
```bash
set PROJECT_ID=<your-project-name>
gcloud projects create %PROJECT_ID% --set-as-default
```

### Project management commands


#### App management
