# Backend

This is the backend of the project. This will contain all python code.

## files

The app.py file is the main file and here are all the endpoints implemented with flask. Here
you will also find the variables for managing the database connection when running the program


The queries.py file contains all the calls to the openAQ API and some parsing of the recieved
data


The process.py file contains all processing functions that handle information to be sent from
flask


The user.py file contains all functions dealing with the user functionalities of the app.


The db_initalization folder contains the code needed to initialize the database. It should only
ne run once and then be left alone. 

## Role

The code in this folder is the code that is needed to query the AQ API, make spatial calculation and
data preparation and then expose that to the frontend (nuxt). The frontend will be able to query the
backend to retrieve data for display and to trigger it to make calculations.

## Running

Open a terminal and navigate to the flaskVueBackend folder. Make sure you have the se4g environment
active. Run:

    flask run

The application should be running on localhost port 5000
