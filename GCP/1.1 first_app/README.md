# Creating our first GCP application
In this section we will introduce how to create an application and deploy it to the GCP. 

## Setting up for the deployment
Our Flask App repository will look like this.
```
flask-app/ 
  ├── main.py 
  ├── app.yaml
  ├── static/
    └── hello.css 
  ├── templates/ 
    ├── hello.html 
    └── 404.html 
  ├── requirements.txt 
  └── README.md
```
Now we need to create the application on the GCP
*Linux*
```bash
gcloud app create --project=${PROJECT_ID}
```
*Windows*
```bash
gcloud app create --project=%PROJECT_ID%
```
An important step is to create an application deployment descriptor which is required for the deployment, one for each application.
```YAML
runtime: python311
handlers:
- url: /static
  static_dir: static
- url: /.*
  secure: always
  script: auto
```
Another important file is the `.gcloudignore`, it specifies which files/directories are not mean for deployment. 
```
.gcloudignore
.git
.gitignore
__pycache__/
env/
venv/
/setup.cfg
```

## Deploying the application
In the CLI withing the application directory context we will input this command.
```bash
gcloud app deploy
```
Let's test
```bash
gcloud app browse
```
> [!NOTE]
> Make sure to have a billing account attached to the project.

> [!WARNING]
> remember to delete the project before going to bed
