# ECS639U Group 19 Coursework

This is the source code for Group 19's coursework in the module ECS639U Web Programming (at Queen Mary University of London). Module leader: Paulo Oliva <[p.oliva@qmul.ac.uk](mailto:p.oliva@qmul.ac.uk)>.

## Openshift Deployment
https://group19-ecs639u-group19.apps.a.comp-teach.qmul.ac.uk

## Collaborators
Name: Taseen Kamil Rahman<br>

Name: Isa Tahir Islam<br>

Name: Lukas Labanok<br>

## Submission Setup Notes
1. Run Django migrations to create the database schema:
   ```console
    python manage.py migrate

    ```
2. Ensure the database is empty using:
   ```console
       python manage.py flush
   
   ```

3. The fixture data can be loaded into the database using the following command.:

   ```console
       python manage.py loaddata initial_data.json
   
   ```

This will include 20 test users and 10 hobbies. It will also include the superuser.

### Superuser Account
Username: admin<br>
Password: england123

### User Accounts
There are 20 accounts with usernames user1, user2...user19, user20.<br>
All have identical passwords: england123


## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Clone this repo to your local machine.

3. Install Pyhton dependencies (main folder):

    ```console
    pip install -r requirements.txt
    ```

4. Install JavaScript dependencies (from 'frontend' folder):

    ```console
    npm install
    ```

5. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    python manage.py runserver
    ```

6. and the Vue server from the 'frontend' sub-folder (only run this for testing frontend.):

    ```console
    npm run dev
    ```
    As the frontend is being served by Django, use:
     ```console
    npm run build
    ```
      If using Windows please see remarks at the bottom and run

    ```console
    $ npm run build-windows
    ```
    This way the frontend is served by Django and is preferred. Note you will have to run a new build every time a change is made - so it may make more sense to develop something on the Vue server beforehand, you just won't have access to the backend. Below it says to do this once it's ready to be deployed, however, this can be safely used in development.

8. Open your browser and go to http://localhost:8000, you will be greeted with a login page, or the template homepage if you are already authenticated.

## OpenShift deployment

Once your project is ready to be deployed you will need to 'build' the Vue app and place it in Django's static folder.

1. The build command in package.json and the vite.config.ts files have already been modified so that when running 'npm run build' (on Mac and Linux) the generated JavaScript and CSS files will be placed in the mainapp static folder, and the index.html file will be placed in the templates folder:

    ```console
    $ npm run build
    ```

    If using Windows please see remarks at the bottom and run

    ```console
    $ npm run build-windows
    ```

2. You should then follow the instruction on QM+ on how to deploy your app on EECS's OpenShift live server.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).


## Running Builds on Windows
As stated in the email from Paulo - this change should already be in our repo but if not:
Please note that the build command included in the group project template works fine on Mac and Linux computers, but will not work on Windows. If you are using a Windows machine, please replace the “scripts” entry with:
```console
"scripts": {

"dev": 
"vite",

"build": 
"vue-tsc && vite build && mv ../api/static/api/spa/index.html ../api/templates/api/spa/.",

"build-windows": 
"vue-tsc && vite build && move ..\\api\\static\\api\\spa\\index.html
 ..\\api\\templates\\api\\spa\\.",

"preview": 
"vite preview"

},
```
and then run

 ```console
    $ npm run build-windows
 ```

instead of “npm run build”. 
