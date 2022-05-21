from flask import Flask
from flask_cors import CORS
import requests
import json

app = Flask(__name__)

#1th try
@app.route('/api/cities/<cityname>', methods=["GET"])
def get_cities(cityname):
    cityEndpoint =f"https://docs.openaq.org/v2/locations?limit=15&page=1&offset=0&sort=desc&radius=1000&country_id=IT&city={cityname}&order_by=lastUpdated&dumpRaw=false"
    # Get the stations
    cities=[]
    nested=[]
    output=[]
    i=1
    r = requests.get(cityEndpoint)
    for result in r.json()['results']:
        try:
            cityname = result['city']
            id=result['id']
            for nested in result['parameters']:    
                # unit=nested['unit']
                # lastValue= nested['lastValue']
                # parameter= nested['parameter']
                # lastUpdated= nested['lastUpdated']
                # parameterId= nested['parameterId']
                try:
                    parameters = {f'parameters {i}': {'lastValue': nested['lastValue'], 'parameter': nested['parameter'],'lastUpdated': nested['lastUpdated'],'parameterId': nested['parameterId'] }}
                except KeyError:
                    continue
                output.append(parameters)
                i+=1
            city={'id':id,'city':cityname ,'parameters':output }
        except KeyError:
            continue
        cities.append(city)
        response = json.dumps({'cities': cities})
    return response

#3 it's working but with the same problem
# @app.route('/api/cities/<cityname>', methods=['GET'])
# def get_cities(cityname):
#     cityEndpoint =f"https://docs.openaq.org/v2/locations?limit=15&page=1&offset=0&sort=desc&radius=1000&country_id=IT&city={cityname}&order_by=lastUpdated&dumpRaw=false"
#     # Get the stations
#     cities=[]
#     # nested=[]
#     output=[]
#     # index=
#     u=1
#     r = requests.get(cityEndpoint)
#     # print('lastValue2=', r.json()['results'][2]['parameters'][2]['lastValue'])
#     for result in (r.json()['results']):
#         try:
#             cityname = result['city']   
#             id=result['id']
#             # print(cityname, id)
#             for nested in range(len(result['parameters'])):
#                 print( result['parameters'][nested])
#                 print(f'lastValue {nested}=', result['parameters'][nested]['lastValue'])
#                 # try:
#                 parameters = {f'para {nested}': {'lastValue': result['parameters'][nested]['lastValue'], 'parameter':result['parameters'][nested]['parameter'],'lastUpdated':result['parameters'][nested]['lastUpdated'],'parameterId': result['parameters'][nested]['parameterId'] }}
#                 # except KeyError:
#                 #     continue
#                 # output.append(parameters)
#             city={'id':id,'city':cityname ,'parameters':parameters }
#         except KeyError:
#             continue
#         cities.append(city)
#         response = json.dumps({'cities': cities})
#     return response

if __name__ == "__main__":
    app.run(debug=True,  use_reloader=False)
    print(get_cities('Milano'))