# Scripts
In this folder you can find all sorts of script that can help you during the excercises or during the exam.

## project_setup_linux
It is a script that sets up the environment variables PROJECT_ID, NAME and GOOGLE_APPLICATION_CREDENTIALS.  
Furthermore, it creates the project, the user and sets up the credentials.  
Finally, it creates a file called "setenv" in which it saves the environment variables used. You may add whatever environment variables you may need in that file.
### Usage
```bash
chmod u+x project_setup_linux
./project_setup_linux
```
The script will output two requests, one that will ask for the PROJECT_ID variable
```bash
Forniscimi il PROJECT_ID
```
to which you will provide an input, let's say `provolo`
```bash
Forniscimi il PROJECT_ID
provolo
Variabile d'ambiente PROJECT_ID settata a provolo
```
then, the same goes for the variable NAME
```bash
Forniscimi ora il NAME dell'utente per cui creerò le credentziali
provoletto
Variabile d'ambiente NAME settata a provoletto
```
Finally, everything will be created and you will have all set up for your project.  
Good luck!