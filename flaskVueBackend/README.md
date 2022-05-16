# Backend

This is the backend of the project. This will contain all python code.

## Terminology

The project will deal with two REST API:s:

- OPEN AQ which stores the data and is queried from this folder. This will be called "the AQ API" or "the API
- The API that this project implements. This will be called "the backend" or "flask"

## Role

The code in this folder is the code that is needed to query the AQ API, make spatial calculation and
data preparation and then expose that to the frontend (nuxt). The frontend will be able to query the
backend to retrieve data for display and to trigger it to make calculations.

## Running

Open a terminal and navigate to the flaskVueBackend folder. Make sure you have the se4g environment
active. Run:

    flask run

The application should be running on localhost port 5000. Check the output of the endpoint by navigating
to http://localhost:5000/api/locations in your browser. 
