from flask import Flask
from flask_cors import CORS
import psycopg2
import requests
import json

MYUSER = 'postgres'
MYPWRD = '123456'
MYPORT = '5433'

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["APPLICATION_ROOT"] = "/"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



@app.before_first_request
def initAPI():
    print("starting setup")

    global cityResponse, cityDict
    cityResponse, cityDict = get_cityNames()
    
    print("setup complete")

# cityDict keys: ['Alessandria', 'Alfonsine', 'Ancona', 'Arezzo', 'Ascoli Piceno', 'Asti', 'Avellino', 'Bari', 'Barletta-Andria-Trani', 'Belluno', 'Benevento', 'Bergamo', 'Biella', 'Bologna', 'Bolzano/Bozen', 'Brescia', 'Brindisi', 'Cagliari', 'Campobasso', 'Carbonia-Iglesias', 'Carpi', 'Caserta', 'Catanzaro', 'Cento', 'Cesena', 'Chiesanuova', 'Civitavecchia', 'Colorno', 'Como', 'Cosenza', 'Cremona', 'Crotone', 'Cuneo', 'Faenza', 'Ferrara', 'Fiorano Modenese', 'Firenze', 'Foggia', "Forli'", "Forli'-Cesena", 'Frosinone', 'Genova', 'Grosseto', 'Guastalla', 'Imola', 'Imperia', 'Jolanda Di Savoia', 'Langhirano', "L'Aquila", 'La Spezia', 'Latina', 'Lecce', 'Lecco', 'Livorno', 'Lodi', 'Lucca', "Lugagnano Val D'Arda", 'Macerata', 'Mantova', 'Massa-Carrara', 'Matera', 'Mezzani', 'Milano', 'Mirandola', 'Modena', 'Molinella', 'Monza E Della Brianza', 'Napoli', 'Novara', 'Nuoro', 'Olbia-Tempio', 'Oristano', 'Ostellato', 'Padova', 'Parma', 'Pavia', 'Perugia', 'Pesaro E Urbino', 'Pescara', 'Piacenza', 'Pisa', 'Pistoia', 'Porretta Terme', 'Potenza', 'Prato', 'Ravenna', 'Reggio Di Calabria', "Reggio Nell'Emilia", 'Rieti', 'Rimini', 'Roma', 'Rovigo', 'Salerno', 'San Clemente', 'San Lazzaro Di Savena', 'San Leo', 'Sassari', 'Sassuolo', 'Savignano Sul Rubicone', 'Savona', 'Siena', 'Sogliano Al Rubicone', 'Sondrio', 'Sorbolo', 'Taranto', 'Teramo', 'Terni', 'Torino', 'Trento', 'Treviso', 'Varese', 'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli', 'Verona', 'Verucchio', 'Vibo Valentia', 'Vicenza', 'Villa Minozzo', 'Viterbo']
def getCityCoords():

    cityString = ""
    for city in cityDict.keys():
        city = city.replace("'","''")
        cityString += "'{}',".format(city)
    cityString += cityString[0:-1]

    query = "SELECT * FROM city WHERE city_name in ({});".format(cityString)

    conn = psycopg2.connect(
    database="SE4G", user = MYUSER, password= MYPWRD, host='localhost', port= MYPORT
    )

    c = conn.cursor()
    c.execute(query)
    res = c.fetchall()
    conn.commit()
    conn.close()

    # Format: cityCoords['city_name'] = [longitude, latitude]
    # The format can be changed through the loop below
    cityCoords = {} 
    for result in res:
        cityCoords[result[1]] = [result[2],result[3]]
    
    return cityCoords





    

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
            location = {'id': result['id'], 'coordinates': [result['coordinates']['longitude'], result['coordinates']['latitude']]}
        except KeyError:
            continue
        locations.append(location)
    
    response = json.dumps({'locations': locations})

    return response
    
#EndPoint for the cities
@app.route('/api/cities') # Moved the actual API call to another function to be able to reuse get_cityNames() elsewhere. 
def serve_cityNames():
    return cityResponse

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

if __name__ == "__main__":
    app.run(debug=True,  use_reloader=False)
    getCityCoords()
    # print(get_locations())
