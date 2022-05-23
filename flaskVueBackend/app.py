from flask import Flask
from flask_cors import CORS
import requests
import json

app = Flask(__name__)

def initialize():
    #Run this when the app starts.
    app.config["DEBUG"] = True
    app.config["APPLICATION_ROOT"] = "/"
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # print(get_locations())

    cities = get_cityNames()

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

@app.route('/api/cities')
def get_cityNames():

    r=requests.get("https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/cities?limit=1000&page=1&offset=0&sort=asc&country=IT&order_by=city")

    citiesname=[]
    # print(r.json()['results'][0])
    # return r.json()
    for result in r.json()['results']:
        try:
            if result['city'] != "unused": #Filtering out the "unused" value that exist in the API. 
                cityname = result['city']
        except KeyError:
            continue
        citiesname.append(cityname)
    response = json.dumps({'cities': citiesname})
    return response

if __name__ == "__main__":
    initialize()