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
    return r.json()
    # for result in r.json()['results']:
    #     try:
    #         location = {'id': result['id'], 'coordinates': {'lat': result['coordinates']['latitude'], 'lng': result['coordinates']['longitude']} }
    #     except KeyError:
    #         continue
    #     locations.append(location)
    # response = json.dumps({'locations': locations})
    # return response

@app.route('/api/cities/<city>', methods=["GET"])
def get_cities(city):
    cityEndpoint =f"https://docs.openaq.org/v2/locations?limit=15&page=1&offset=0&sort=desc&radius=1000&country_id=IT&city={city}&order_by=lastUpdated&dumpRaw=false"
    # Get the stations
    r = requests.get(cityEndpoint)
    print (f"{city}")
    return r.json()

@app.route('/api/latests/<location_id>', methods=["GET"])
def get_latests(location_id):
    stationEndpoint =f"https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/latest/{location_id}?limit=100&page=1&offset=0&sort=desc&radius=1000&country=IT&order_by=lastUpdated&dumpRaw=false"
    # Get the stations
    r = requests.get(stationEndpoint)
    print (f"{location_id}")
    return r.json()

# If I am able to return the last updated date and relative parameter of each value.
    # print(r.json()['results'][0])
    # stations= []
    # param = []
    # lastUp = []
    # for result in r.json()['results']:
    #     for m in result['measurements']:
    #         # param.append(m['parameter'])
    #         try:
    #             station = {{'lastUpdated': m['lastUpdated'], 'parameter': m['parameter']}}
    #         except KeyError:
    #             continue
    #         lastUp.append('lastUpdated')
    #     return (r.json(),lastUp)
   
if __name__ == "__main__":
    app.run(debug=True,  use_reloader=False)
    # print(get_cities("Milano"))
    