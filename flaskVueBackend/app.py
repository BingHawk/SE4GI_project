from flask import Flask
from flask_cors import CORS
import requests
import json

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

if __name__ == "__main__":
    print(get_locations())