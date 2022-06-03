from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import requests

from historical import getMonthData, getYearData

#### GLOBAL VARIABLES
MYUSER = 'postgres'
MYPWRD = 'blod'
MYPORT = '5432'

#### FLASK CONFIGURATION
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["APPLICATION_ROOT"] = "/"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# schema for result of get_locations:
"""
{locations: [
    {
    "cityName": "city1",
    "Coordinates": [lng, lat],
    "particles": [
        {
        "particleName", "particle1",
        "value": value,
        "unit": unit
        "lastupdate": DateTime,
        },
        {
        "particleName", particle2,
        "value": value,
        "unit": unit
        "lastupdate": DateTime,
        },
        ...
        ]
    },
    {
    "cityName": "city1",
    "Coordinates": [lng, lat],
    "particles": [
        {
        "particleName", "particle1",
        "value": value,
        "unit": unit
        "lastupdate": DateTime,
        },
        {
        "particleName", particle2,
        "value": value,
        "unit": unit
        "lastupdate": DateTime,
        },
        ...
        ]
    },
    ...
    ]
}

"""
@app.route('/api/locations', methods=["GET"])
def get_locations():
    # the endpoint of meassuring stations in italy
    italyEndpoint = "https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/locations?limit=10000&page=1&offset=0&sort=desc&radius=10000&country_id=it&order_by=lastUpdated&dumpRaw=false"
    
    # Get the stations
    r = requests.get(italyEndpoint)
    locations = []
    for result in r.json()['results']:
        try:
            location = {
                'id': result['id'],
                'cityName': result['name'], # Not correct, this is the name of the station. 
                'coordinates': [result['coordinates']['longitude'],result['coordinates']['latitude']],
                'particles': []
                }
            for parameter in result['parameters']:
                particle = {
                    'particleName': parameter['displayName'],
                    'value': parameter['lastValue'],
                    'unit': parameter['unit'],
                    'lastUpdate': parameter['lastUpdated'], # string with datetime format from openAQ. ex: '2022-05-25T12:02:59+00:00'
                }
                location['particles'].append(particle)
        except KeyError:
            continue
        locations.append(location)
    
    response = jsonify({'locations': locations})

    return response

@app.route('/api/month/<city>', methods = ['GET'])
def serveMonthData(city):
    try:
        city = cityDict[city.title()][0]
    except KeyError:
        return "City {} does not exist in database".format(city.title()), 400
    
    res = getMonthData(city)
    return jsonify(res)

@app.route('/api/year/<city>', methods = ['GET'])
def serveYearData(city):
    try:
        city = cityDict[city.title()][0]
    except KeyError:
        return "City {} does not exist in database".format(city.title()), 400

    res = getYearData(city)
    return jsonify(res)

# Returns latest value for every city.
@app.route('/api/latest', methods=["GET"])
def get_latest():
    #endpoint for latest values of meassuring stations in italy
    latestEndpoint = 'https://api.openaq.org/v2/latest?limit=1000&page=1&offset=0&sort=desc&radius=1000&country_id=IT&order_by=lastUpdated&dumpRaw=false'
    
    #get values
    r = requests.get(latestEndpoint)
    
    locations = {}
    for result in r.json()['results']:
        if result['city'] == None:
            continue
        else:
            city = result['city']
        if city in locations.keys():
            for particle in locations[city]['particles']:
                for particle_in in result['measurements']:
                    if particle['parameter'] == particle_in['parameter']:
                        if isinstance(particle['value'], list):
                            particle['value'].append(particle_in['value'])
                        else:
                            particle['value'] = [particle['value']]
                            particle['value'].append(particle_in['value'])
        else:
            locations[city] = {'cityName': city, 'particles': result['measurements']}       
        
    for city in locations.keys():
        for particle in locations[city]['particles']:
            if isinstance(particle['value'], list):
               n = len(particle['value'])
               mean_l = sum(particle['value'])/n
               particle['value'] = mean_l  

    for city in getCityCoords().keys():
            coords = getCityCoords()
            locations[city] = {'cityName': city, 'coordinates': coords[city], 'particles': result['measurements']}
               
    locations = list(locations.values())
    response = {'locations': locations}
        
    return jsonify(response)
    
#EndPoint for the cities
@app.route('/api/cities', methods = ['GET']) # Moved the actual API call to another function to be able to reuse get_cityNames() elsewhere. 
def serve_cityNames():
    return jsonify(cityResponse)



#### RUNNING FLASK IN DEV MODE
if __name__ == "__main__":
    app.run(debug=True,  use_reloader=False)
    # print(get_locations())
