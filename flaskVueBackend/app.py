from flask import Flask
from flask_cors import CORS
import requests
import json

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
    
    response = json.dumps({'locations': locations})

    return response

if __name__ == "__main__":
    print(get_locations())