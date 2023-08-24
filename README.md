# SoftDesk RESTful API

This is a project done as part of my degree program at Openclassrooms (project 10: Créez une API sécurisée RESTful en utilisant Django REST).

The objective is to create a RESTful API for reporting and tracking technical problems.

## Prerequisite
### Create a virtual environment

Requirement : Python3.3 or later

Open a terminal at the root of the project directory, and enter the following command:

    python -m venv <name of the virtual environment>

For example:

    python -m venv env

This will create a directory named *env* inside your project directory.

### Activate the virtual environment

In the project directory, open a terminal and enter the following command:

    source <name of the virtual environment>/bin/activate


## Run the website
+ Download or clone the repository.
+ Inside the project directory, open your terminal and enter the following command:

    `pip install -r requirements.txt`

    This will install all the required modules to run the application. Those are Django and Pillow.

+ Again, inside the project directory, in your terminal and enter the following command:

    `python manage.py runserver`

You will see an output similar to the following in the commandline:

    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    July 25, 2023 - 21:17:12
    Django version 3.2.18, using settings 'litreviewbooks.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    
You have just started the Django development server. Now that the server’s running, visit http://127.0.0.1:8000/ with your web browser to test the application.



