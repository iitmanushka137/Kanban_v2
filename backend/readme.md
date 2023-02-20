# Local Setup
- Run ```pip install -r requirements.txt``` to install all dependencies written in ```requirements.txt``` which is inside ```backend``` folder

# Local Development Run
- ```python3 app.py``` It will start the flask app in ```development```. This is for running app on local system.
- ```npm run serve``` for serving the app from frontend on Vue

# Folder Structure of ```backend```
- ```project.sqlite3``` is the sqlite database. It can be anywhere on the machine, just the adjustment in the path in ```app.py``` is required. One of the database is shipped for testing.
- The application code for my app is ```/```
- ```templates``` is the default folder where templates are stored which is used for sending mails.
- ```application``` contains the ```api```, ```cache.py```, ```clry.py```, ```emailgen.py```, ```models.py```, ```tasks.py``` and ```static``` folder.
- ```static``` a folder in which we have ```IMG``` folder which has images used in the app. Also the graphs generated are saved in it which is further encoded to send to frontend and decoded over there.
- ```Project Documentation``` having a brief description about app
- A ```readme``` file and ```requirements``` file

# Folder Structure of ```frontend```
- ```node_modules``` required for running VueJS CLI
- ```public``` having public components
- ```src``` is the default folder where frontend components and routers are located.
- ```components``` which has vue components for frontend, ```router``` which contains ```index.js``` for defining different routes, ```App.vue``` the page on which app is being served, ```index.js``` for app start and ```store``` to create the store for vue.
- A ```readme``` file and other required configurations.

```
Project
├── backend
|   ├── requirements.txt
|   ├── readme.md
|   ├── project.sqlite3
|   ├── Project Documentation.pdf
|   ├── app.py
|   ├── templates
|   |       ├── cards_csv.html
|   |       ├── daily_reminder.html
|   |       ├── list_csv.html
|   |       └── monthly_report.html
|   └── application
|          ├── api.py
|          ├── cache.py
|          ├── clry.py
|          ├── emailgen.py
|          ├── models.py
|          ├── tasks.py
|          └── static
|               └── IMG
|               
├── frontend/
│   ├── public
|   ├──src
|   |    ├── components
|   |    |      ├── CardAdding.vue
|   |    |      ├── CardDelete.vue
|   |    |      ├── CardUpdating.vue
|   |    |      ├── DeleteList.vue
|   |    |      ├── HomePage.vue
|   |    |      ├── ListAdding.vue
|   |    |      ├── LoginPage.vue
|   |    |      ├── RegisterPage.vue
|   |    |      ├── SummaryPg.vue
|   |    |      └── UpdateList.vue
|   |    ├── router/index.js
|   |    ├── store/inex.js
|   |    ├── App.vue
|   |    └── main.js
|   ├── .gitignore
|   ├── babel.config.js
|   ├── jsconfig.json
|   ├── package-lock.json
|   ├── package.json
|   ├── README.md
|   └── vue.config.js
└── Kanban.yaml
```