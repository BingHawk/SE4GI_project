from asyncio import create_task
from flask import Flask, jsonify
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
    
#EndPoint for the cities
@app.route('/api/cities') # Moved the actual API call to another function to be able to reuse get_cityNames() elsewhere. 
def serve_cityNames():
    response, cityDict = get_cityNames()
    return response

def get_cityNames():

    r=requests.get("https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/cities?limit=1000&page=1&offset=0&sort=asc&country=IT&order_by=city")

    citiesname=[]
    cityDict = {} # Maps recapitalized city names to their original caputalization. 
    # print(r.json()['results'][0])
    # return r.json()
    for result in r.json()['results']:
        try:
            if result['city'] != "unused": #Filtering out the "unused" value that exist in the API. 
                cityname = result['city'].title() #Forcing one capitalization policy
                if cityname in cityDict.keys(): # Filling the cityDict with lists, as there are sometimes two endpint entries per city. 
                    cityDict[cityname].append(result['city'])
                else: 
                    cityDict[cityname] = [result['city']]
                # print(result['city'])
        except KeyError:
            continue
        if cityname not in citiesname: #Avoiding adding duplicates
            citiesname.append(cityname)

    response = json.dumps({'cities': citiesname})
    return response, cityDict

# the average as well as the parameters work finally!
@app.route('/api/cities/<cityname>', methods=["GET"])
def get_cities(cityname):
    cityEndpoint =f"https://api.openaq.org/v2/locations?limit=15&page=1&offset=0&sort=desc&radius=1000&country_id=IT&city={cityname}&order_by=lastUpdated&dumpRaw=false"
    # Get the stations
    parameters=[]
    r = requests.get(cityEndpoint)
    parNO2, paro3, parco, parso2, parpm10, parpm25, parbc, parpm1, parnox, parch4, parufp, parno, parco2, parum010, parum025, parum100, parpm4 = ([] for i in range(17))
    for result in r.json()['results']:
        cityName = result['city']   
        id=result['id']
        lastUpdate=result['lastUpdated']
        for value in result['parameters']:
            print(value['parameter'])
            print(value['lastValue'])
            if value['parameter']== 'no2':
                parNO2.append(value['lastValue'])
            elif value['parameter']== "o3":
                paro3.append(value['lastValue'])
            elif value['parameter']== "co":
                parco.append(value['lastValue'])
            elif  value['parameter']== "so2":
                parso2.append(value['lastValue'])
            elif  value['parameter']== "pm10":
                parpm10.append(value['lastValue'])
            elif  value['parameter']== "pm25":
                parpm25.append(value['lastValue'])
            elif  value['parameter']== "bc":
                parbc.append(value['lastValue'])
            elif  value['parameter']== "pm1":
                parpm1.append(value['lastValue'])
            elif  value['parameter']== "nox":
                parnox.append(value['lastValue'])
            elif  value['parameter']== "ch4":
                parch4.append(value['lastValue'])
            elif  value['parameter']== "ufp":
                parufp.append(value['lastValue'])
            elif  value['parameter']== "no":
                parno.append(value['lastValue'])
            elif  value['parameter']== "co2":
                parco2.append(value['lastValue'])
            elif  value['parameter']== "um010":
                parum010.append(value['lastValue'])
            elif  value['parameter']== "um025":
                parum025.append(value['lastValue'])
            elif  value['parameter']== "um100":
                parum100.append(value['lastValue'])
            elif  value['parameter']== "pm4":
                parpm4.append(value['lastValue'])
            else:
                print('new parameter')
    d={"no2":parNO2, "o3":paro3, "co":parco, "so2":parso2, "pm10":parpm10, "pm25":parpm25, "bc":parbc, "pm1":parpm1, "nox":parnox , "ch4":parch4, "ufp":parufp , "no":parno, "co2":parco2 , "um010":parum010 , "um025":parum025 , "um100":parum100 , "pm4":parpm4}
    for key, item in d.items():
        try:
            average= sum(item)/len(item)         
        except ZeroDivisionError:
            average= None
        parametr = {'particleName': key,  'unit': 	"µg/m³" , 'value': average}
        parameters.append(parametr)
    city={'id':id,'city':cityName , 'lastUpdate':lastUpdate,'Measurements':parameters }
    response = jsonify({'cities': city})
    return response  

if __name__ == "__main__":
    app.run(debug=True,  use_reloader=False)
    print(get_locations())
