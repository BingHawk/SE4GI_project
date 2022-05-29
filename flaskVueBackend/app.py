from asyncio import create_task
from flask import Flask
from flask_cors import CORS
import requests
import json
import psycopg2

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["APPLICATION_ROOT"] = "/"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/locations', methods=["GET"])
def get_locations():
    # the endpoint of meassuring stations in italy
    italyEndpoint = "https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/locations?limit=10000&page=1&offset=0&sort=desc&radius=10000&country_id=it&order_by=lastUpdated&dumpRaw=false"
    
    # Get the stations
    r = requests.get(italyEndpoint)

    locations = []
    print(r.json()['results'][0])
    for result in r.json()['results']:
        try:
            location = {'id': result['id'], 'coordinates': {'lat': result['coordinates']['latitude'], 'lng': result['coordinates']['longitude']} }
        except KeyError:
            continue
        locations.append(location)
    
    response = json.dumps({'locations': locations})

    return response

#create the database table
def addCitiesToDatabase(cities):
    conn = psycopg2.connect(
   database="SE4G", user='postgres', password='123456', host='localhost', port= '5433'
)
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Doping EMPLOYEE table if already exists.
    cursor.execute("DROP TABLE IF EXISTS CITY")

    #Creating table as per requirement
    createTable ='''CREATE TABLE CITY(
    CITY_NAME CHAR(20) NOT NULL,
    NORTH FLOAT,
    EAST FLOAT
    )'''
    cursor.execute(createTable)
    #print("Table created successfully........")
    conn.commit()
    #Closing the connection
    conn.close()
    
    
#EndPoint for the cities
@app.route('/api/cities')
def get_cityName():
    r=requests.get("https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/cities?limit=1000&page=1&offset=0&sort=asc&country=IT&order_by=city")
    citiesname=[]
    for result in r.json()['results']:
        try:
            cityname = result['city']
        except KeyError:
            continue
        citiesname.append(cityname)
    response = json.dumps({'cities': citiesname})
    addCitiesToDatabase(citiesname)
    return response

if __name__ == "__main__":
    app.run(debug=True,  use_reloader=False)
    print(get_locations())